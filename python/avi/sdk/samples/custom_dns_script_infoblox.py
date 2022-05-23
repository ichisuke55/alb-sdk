
############################################################################
# ========================================================================
# Copyright 2022 VMware, Inc.  All rights reserved. VMware Confidential
# ========================================================================
###
"""
This script allows the user to communicate with Infoblox DNS provider.

Required Functions
------------------
1. CreateOrUpdateDnsRecords: Function to create or update DNS records with the provider.
2. DeleteDnsRecords: Function to delete DNS records from the provider.

Required Exception Classes
--------------------------
1. CustomDnsAuthenticationErrorException: Raised when authentication fails.
2. CustomDnsRecordNotFoundException: Raised when given record not found, incase of update record request.
3. CustomDnsRecordAlreadyExistsException: Raised when the record already exists.
4. CustomDnsGeneralException: Raised for other types of exceptions.

Helper Functions (Optional)
---------------------------
1. _verify_required_fields_in_auth_params: Internal function used to verify that all required auth parameters are provided.
2. _check_and_raise_auth_error: Internal function used to raise an exception if authentication fails.
3. _build_ipvxaddrs_objects: Internal function used to build ipv4addrs and ipv6addrs objects for payload data from a given list of ips.
4. _get_ips_by_host: Internal function used to return ips for a given record name.
5. _create_dns_record: Internal function used to create a DNS record with the provider.
6. _update_dns_record: Internal function used to update a given DNS record with the provider.
7. _delete_dns_record: Internal function used to delete a given DNS record from the provider.
"""

from types import new_class
import requests
import json
import logging
import copy
from bs4 import BeautifulSoup


class CustomDnsAuthenticationErrorException(Exception):
    """
    Raised when authentication fails.
    """
    pass

class CustomDnsRecordNotFoundException(Exception):
    """
    Raised when given record not found, incase of update record request.
    """
    pass

class CustomDnsRecordAlreadyExistsException(Exception):
    """
    Raised when the record already exists.
    """
    pass

class CustomDnsGeneralException(Exception):
    """
    Raised for other types of exceptions.
    """
    pass


def _check_and_raise_auth_error(response):
    """
    Function to check authentication error for a given response and raise an exception for the same.
    """
    if response.status_code in [401, 403]:
        text = BeautifulSoup(response.text, 'html.parser').text
        raise CustomDnsAuthenticationErrorException(response.reason, response.status_code, response.url, text)


def _verify_required_fields_in_auth_params(auth_params):
    """
    Function to verify that all required auth parameters are provided.
    """
    logger = logging.getLogger(auth_params.get('logger_name', ''))
    missing_req_params = []
    if 'server' not in auth_params:
        missing_req_params.append('server')
    if 'username' not in auth_params:
        missing_req_params.append('username')
    if 'password' not in auth_params:
        missing_req_params.append('password')
    if 'wapi_version' not in auth_params:
        missing_req_params.append('wapi_version')
    if missing_req_params:
        missing_req_params = ', '.join(missing_req_params)
        logger.error("all credentials are not provided, missing parameters[%s]" % missing_req_params)
        raise CustomDnsGeneralException("all credentials are not provided, missing parameters[%s]" % missing_req_params)


def _build_ipvxaddrs_objects(ips):
    """
    Function to build ipv4addrs and ipv6addrs objects for payload data from a given list of ips.
    """
    ipv4addrs = []
    ipv6addrs = []
    if ips['v4_ips']:
        for v4_ip in ips['v4_ips']:
            ipv4addrs.append({'ipv4addr': v4_ip})
    if ips['v6_ips']:
        for v6_ip in ips['v6_ips']:
            ipv6addrs.append({'ipv6addr': v6_ip})
    return ipv4addrs, ipv6addrs


def _get_ips_by_host(auth_params, record_name, ip_type='V4_V6'):
    """
    Function to return ips for a given record name.
    """
    username = auth_params.get('username')
    password = auth_params.get('password')
    server = auth_params.get('server')
    wapi_version = auth_params.get('wapi_version')
    dns_view = auth_params.get('dns_view', 'default')
    logger = logging.getLogger(auth_params.get('logger_name', ''))

    rest_url = 'https://' + server + '/wapi/' + wapi_version + \
            '/record:host?name=' + record_name + '&view=' + dns_view
    ipaddrs = []
    try:
        r = requests.get(url=rest_url, auth=(username, password), verify=False)
        _check_and_raise_auth_error(r)
        logger.info("record_name[%s], GET req[%s] status_code[%s]" % (record_name, rest_url, r.status_code))
        r_json = r.json()
        err_msg = str(r.status_code)
        if r.status_code == 200:
            if len(r_json) > 0:
                if ip_type == 'V4_ONLY' or ip_type == 'V4_V6':
                    if 'ipv4addrs' in r_json[0] and len(r_json[0]['ipv4addrs']) > 0:
                        for ipv4addr in r_json[0]['ipv4addrs']:
                            ipaddrs.append(ipv4addr['ipv4addr'])
                if ip_type == 'V6_ONLY' or ip_type == 'V4_V6':
                    if 'ipv6addrs' in r_json[0] and len(r_json[0]['ipv6addrs']) > 0:
                        for ipv6addr in r_json[0]['ipv6addrs']:
                            ipaddrs.append(ipv6addr['ipv6addr'])
                return ipaddrs
            else:
                err_msg += ": No host records found!"
        else:
            err_msg += ' : '  + r_json['text'] if 'text' in r_json else ''
            raise CustomDnsGeneralException(err_msg)
    except CustomDnsAuthenticationErrorException as e:
        raise
    except Exception as e:
        logger.error("error retrieving ips for a host record[%s] reason[%s]" %(record_name, str(e)))
        raise CustomDnsGeneralException("error retrieving ips for a host record[%s] reason[%s]" %(record_name, str(e)))

    
def _create_dns_record(auth_params, record_name, ips):
    """
    Function to create a DNS record.
    """
    username = auth_params.get('username')
    password = auth_params.get('password')
    server = auth_params.get('server')
    wapi_version = auth_params.get('wapi_version')
    dns_view = auth_params.get('dns_view', 'default')
    
    logger = logging.getLogger(auth_params.get('logger_name', ''))
    ipv4addrs, ipv6addrs = _build_ipvxaddrs_objects(ips)
    rest_url = 'https://' + server + '/wapi/' + wapi_version + '/record:host?_return_fields=ipv4addrs,ipv6addrs'
    payload = json.dumps({'name': record_name,'view': dns_view, 'ipv4addrs': ipv4addrs, 'ipv6addrs': ipv6addrs })
    
    try:
        r = requests.post(url=rest_url, auth=(username, password),
                    verify=False, data=payload)
        _check_and_raise_auth_error(r)
        logger.info("record_name[%s], POST req[%s %s] status_code[%s]" % (record_name, rest_url, payload, r.status_code))
        r_json = r.json()
        if r.status_code == 200 or r.status_code == 201:
            return
        elif r.text and 'already exists' in r_json['text']:
            host_ips = _get_ips_by_host(auth_params, record_name)
            logger.info("record_name[%s], record ips on infoblox[%s]" %(record_name, host_ips))
            if set(ips['v4_ips']).issubset(set(host_ips)) and set(ips['v6_ips']).issubset(set(host_ips)):
                logger.info("record name[%s] for ipv4addrs %s and ipv6addrs %s already exists."%
                            (record_name, ips['v4_ips'], ips['v6_ips']))
            else:
                raise CustomDnsRecordAlreadyExistsException(r_json['text'])
    except CustomDnsAuthenticationErrorException as e:
        raise
    except CustomDnsRecordAlreadyExistsException as e:
        raise CustomDnsRecordAlreadyExistsException("record[%s] reason[%s]" %(record_name, str(e)))
    except Exception as e:
        logger.error("Error creating dns record %s on Infoblox, req[%s %s] rsp[%s]" %
                        (record_name, rest_url, payload, str(e)))
        raise CustomDnsGeneralException("Error creating dns record %s on Infoblox, reason[%s]" %(record_name, str(e)))


def _update_dns_record(auth_params, record_name, ips):
    """
    Function to update a given DNS record.
    """
    username = auth_params.get('username')
    password = auth_params.get('password')
    server = auth_params.get('server')
    wapi_version = auth_params.get('wapi_version')
    dns_view = auth_params.get('dns_view', 'default')
    
    logger = logging.getLogger(auth_params.get('logger_name', ''))
    ipv4addrs, ipv6addrs = _build_ipvxaddrs_objects(ips)
    payload = json.dumps({'name': record_name,'view': dns_view, 'ipv4addrs': ipv4addrs, 'ipv6addrs': ipv6addrs })

    # Get the reference of the dns record
    host_ref = None
    rest_url = 'https://' + server + '/wapi/' + wapi_version + '/record:host?name=' + record_name
    try:
        r = requests.get(url=rest_url, auth=(username, password), verify=False)
        _check_and_raise_auth_error(r)
        logger.info("record_name[%s], GET req[%s] status_code[%s]" % (record_name, rest_url, r.status_code))
        r_json = r.json()
        if r.status_code == 200:
            host_ref = r_json[0]['_ref'] if len(r_json) > 0 and r_json[0]['_ref'] else None
        else:
            err_msg = str(r.status_code) + (' : '  + r_json['text'] if 'text' in r_json else '')
            raise CustomDnsGeneralException(err_msg)
    except CustomDnsAuthenticationErrorException as e:
        raise
    except Exception as e:
        logger.error("Error retrieving the record[%s] reason[%s]" % (record_name, str(e)))
        raise CustomDnsGeneralException("Error retrieving the record[%s] reason[%s]" % (record_name, str(e)))
    
    # Raise an error message if the record not found
    if not host_ref:
        err_msg = "record[%s] not found!" % record_name
        logger.error(err_msg)
        raise CustomDnsRecordNotFoundException(err_msg)

    rest_url = 'https://' + server + '/wapi/' + wapi_version + '/' + host_ref + '?_return_fields=ipv4addrs,ipv6addrs'
    try:
        r = requests.put(url=rest_url, auth=(username, password),
                    verify=False, data=payload)
        _check_and_raise_auth_error(r)
        logger.info("record_name[%s], PUT req[%s %s] status_code[%s]" % (record_name, rest_url, payload, r.status_code))
        r_json = r.json()
        if r.status_code == 200 or r.status_code == 201:
            return
        elif 'text' in r_json:
            raise CustomDnsGeneralException(r_json['text'])
    except CustomDnsAuthenticationErrorException as e:
        raise
    except Exception as e:
        logger.error("Error updating dns record %s on Infoblox, req[%s %s] rsp[%s]" %
                        (record_name, rest_url, payload, str(e)))
        raise CustomDnsGeneralException("Error updating dns record %s on Infoblox, reason[%s]" %(record_name, str(e)))


def _delete_dns_record(auth_params, record_name):
    """
    Function to delete a given DNS record.
    """
    username = auth_params.get('username')
    password = auth_params.get('password')
    server = auth_params.get('server')
    wapi_version = auth_params.get('wapi_version')
    dns_view = auth_params.get('dns_view', 'default')
    
    logger = logging.getLogger(auth_params.get('logger_name', ''))
    rest_url = 'https://' + server + '/wapi/' + wapi_version +'/record:host?name=' + record_name

    try:
        # Get the reference of the dns record
        r = requests.get(url=rest_url, auth=(username, password), verify=False)
        _check_and_raise_auth_error(r)
        logger.info("record_name[%s], GET req[%s] status_code[%s]" % (record_name, rest_url, r.status_code))
        r_json = r.json()
        host_ref = None
        err_msg = "record[%s] not found!" % record_name
        if r.status_code == 200:
            host_ref = r_json[0]['_ref'] if len(r_json) > 0 and r_json[0]['_ref'] else None
            if not host_ref:
                logger.info(err_msg)
                return
            
            # Delete the record
            rest_url = 'https://' + server + '/wapi/' + \
                wapi_version + '/' + host_ref
            r = requests.delete(url=rest_url, auth=(username, password), verify=False)
            _check_and_raise_auth_error(r)
            logger.info("record_name[%s], DELETE req[%s] status_code[%s]" % (record_name, rest_url, r.status_code))
            r_json = r.json()
            if r.status_code == 200:
                return
        if 'text' in r_json:
            err_msg = str(r.status_code) + BeautifulSoup(r.text, 'html.parser').text
        logger.error(err_msg)
        raise CustomDnsGeneralException(err_msg)
    except CustomDnsAuthenticationErrorException as e:
        raise
    except Exception as e:
        logger.error("Error deleting the record[%s] reason[%s]" % (record_name, str(e)))
        raise CustomDnsGeneralException("Error deleting the record[%s] reason[%s]" % (record_name, str(e)))


def DeleteDnsRecords(records_info, auth_params):
    """
    Function to delete DNS records from the provider.
    Args
    ----
        auth_params: (dict of str: str)
            Parameters required for authentication.
        record_info: (dict of str: dict)
            Records information with following keys.
            ips (dict of str: list of str): Keys are 'v4_ips' and 'v6_ips', values are list of IPs for each.
            dns_info (dict of str: dict): Keys are FQDNs, value contains FQDN metadata such as TTL, record type, etc,.
    Returns
    -------
        Return true on success.
    Raises
    ------
        CustomDnsAuthenticationErrorException: if authentication fails.
        CustomDnsGeneralException: if api request fails for any other reason.
    """
    _verify_required_fields_in_auth_params(auth_params)
    logger = logging.getLogger(auth_params.get('logger_name', ''))
    tmp_auth_params = copy.deepcopy(auth_params)
    tmp_auth_params['password'] = '<sensitive>'
    logger.info("records_info %s, auth_params %s"%(records_info, tmp_auth_params))
    for fqdn in records_info['dns_info'].keys():
        _delete_dns_record(auth_params, fqdn)
    return True


def CreateOrUpdateDnsRecords(new_records_info, old_records_info, auth_params):
    """
    Function to create/update DNS records with the provider.
    Args
    ----
        auth_params: (dict of str: str)
            Parameters required for authentication.
        new_record_info: (dict of str: dict)
            New records information with following keys.
            ips (dict of str: list of str): Keys are 'v4_ips' and 'v6_ips', values are list of IPs for each.
            dns_info (dict of str: dict): Keys are FQDNs, value contains FQDN metadata such as TTL, record type, etc,.
        old_record_info: (dict of str: dict)
            Old records information with following keys.
            ips (dict of str: list of str): Keys are 'v4_ips' and 'v6_ips', values are list of IPs for each.
            dns_info (dict of str: dict): Keys are FQDNs, value contains FQDN metadata such as TTL, record type, etc,.
    Returns
    -------
        Returns true on success.
    Raises
    ------
        CustomDnsAuthenticationErrorException: if authentication fails.
        CustomDnsRecordAlreadyExistsException: if the record already exists.
        CustomDnsRecordNotFoundException: if the record not found, in case of update record request.
        CustomDnsGeneralException: if api request fails for any other reason.
    """
    _verify_required_fields_in_auth_params(auth_params)
    logger = logging.getLogger(auth_params.get('logger_name', ''))
    tmp_auth_params = copy.deepcopy(auth_params)
    tmp_auth_params['password'] = '<sensitive>'
    logger.info("new_records_info[%s], old_records_info[%s], auth_params[%s]"%(
                new_records_info, old_records_info,  tmp_auth_params))
    
    # Compare new_records_info and old_records_info, and accordingly 
    # perform create/update/delete action on the records.
    
    # Step 1. If new_records_info is empty, then delete all records in the old_records_info.
    # Happens in errback case or in vsvip update case where all DNS info is removed.
    if not new_records_info:
        DeleteDnsRecords(old_records_info, auth_params)
        return True

    # Step 2. If old_records_info is empty, then create all records in the new_records_info.
    if not old_records_info:
        for fqdn in new_records_info['dns_info'].keys():
            _create_dns_record(auth_params, fqdn, new_records_info['ips'])
        return True
    
    if new_records_info == old_records_info:
        logger.info("Both new_records_info and old_records_info are same, ignoring this action")
        return 

    # Step 3. If both new_records_info and old_records_info are not empty, 
    # compare both and perform required actions.
    # Step 3a. Perform create record operation for newly added fqdns 
    # and update record operation for updated fqdns.
    new_records = set(new_records_info['dns_info'].keys())
    old_records = set(old_records_info['dns_info'].keys())
    added_fqdns = new_records.difference(old_records)
    deleted_fqdns = old_records.difference(new_records)
    updated_fqdns = []
    if new_records_info['ips'] != old_records_info['ips']:
        updated_fqdns = new_records.intersection(old_records)
    logger.info("added fqdns[%s], updated fqdns[%s], deleted fqdns[%s]"%(added_fqdns, updated_fqdns, deleted_fqdns))
    for fqdn in added_fqdns:
        _create_dns_record(auth_params, fqdn, new_records_info['ips'])
    for fqdn in updated_fqdns:
        _update_dns_record(auth_params, fqdn, new_records_info['ips'])

    # Step 3b. Check for deleted fqdns and perform delete record operation for deleted fqdns.
    deleted_fqdns_record_info = {}
    deleted_fqdns_record_info['dns_info'] = {}
    deleted_fqdns_record_info['ips'] = old_records_info['ips']
    for fqdn in deleted_fqdns:
        deleted_fqdns_record_info['dns_info'][fqdn] = old_records_info['dns_info'][fqdn]
    if deleted_fqdns_record_info:
        DeleteDnsRecords(deleted_fqdns_record_info, auth_params)
    return True 