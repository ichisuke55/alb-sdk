from avi.sdk.avi_api import ApiSession, \
    sessionDict, APIError
import requests
import re
import urllib
# import urlparse
import json
from datetime import datetime
from requests import ConnectionError
from requests.exceptions import ChunkedEncodingError
from ssl import SSLError
import time
import logging

logger = logging.getLogger(__name__)


class OneloginSAMLApiSession(ApiSession):
    """
    Extends the ApiSession class to override authentication
    method and provide helper utilities to work with Avi
    Controller and IDPs like onelogin, okta, etc.
    """

    SAML_URL_SUFFIX = "/sso/login"
    # Request RegX
    saml_request_regex = r'<input type=\"hidden\" ' \
                         r'name=\"SAMLRequest\" value=\"(.*?)\"'
    request_relay_state_regex = r'<input type=\"hidden\" ' \
                                r'name=\"RelayState\" value=\"(.*?)\"'
    request_assertion_url_regex = r'<form method=\"post\" action=\"(.*?)\">'
    # Response RegX
    saml_response_regex = r'<input type=\"hidden\" ' \
                          r'name=\"SAMLResponse\" value=\"(.*?)\"'
    response_relay_state_regex = r'<input type=\"hidden\" ' \
                                 r'name=\"RelayState\" value=\"(.*?)\"'
    response_assertion_url_regex = r'<form method=\"post\" ' \
                                   r'action=\"(.*?)\">'

    def __init__(self, controller=None, username=None, password=None,
                 token=None, tenant=None, tenant_uuid=None, verify=False,
                 port=None, timeout=60, api_version=None,
                 retry_conxn_errors=True, data_log=False,
                 avi_credentials=None, session_id=None, csrftoken=None,
                 lazy_authentication=False, max_api_retries=None,
                 idp_cookies=None,user_hdrs=None):
        """
        This extends ApiSession class and overrides authentication method
        for SMAL authentication.

        :param controller: Controller IP
        :param username: IDP username
        :param password: IDP password
        :param token: Controller token
        :param tenant: Overrides the tenant used during session creation
        :param tenant_uuid: Overrides the tenant or tenant_uuid during session
            creation
        :param verify: Boolean flag for SSL verification of url
        :param port: Controller SSO port
        :param timeout: Timeout for API calls; Default value is 60 seconds
        :param api_version: Overrides x-avi-header in request header during
            session creation
        :param retry_conxn_errors: Retry on connection errors
        :param data_log: Data log
        :param avi_credentials: avi_credential object
        :param session_id: Session ID
        :param csrftoken: CSRF Token
        :param lazy_authentication: Lazy_authentication for controller.
        :param max_api_retries: Maximum API retires
        :param idp_cookies: IDP cookies if want to use existing IDP session
        """

        self.idp_cookies = idp_cookies
        super(OneloginSAMLApiSession, self).__init__(
            controller, username, password, token,
            tenant, tenant_uuid, verify,
            port, timeout, api_version,
            retry_conxn_errors, data_log,
            avi_credentials, session_id, csrftoken,
            lazy_authentication, max_api_retries, user_hdrs)
        return

    def saml_assertion(self, username, password):
        """
        Perform SAML request from controller to IDPs.
        Establish session with controller and IDP.
        Assert SAML request into the reqeust.
        Get the controller session and IDP session.

        :param username: IDP Username
        :param password: IDP Password
        :return: controller session and IDP response
        """

        # Getting controller session
        controller_session = requests.Session()
        controller_session.verify = False
        saml_controller_url = self.prefix + self.SAML_URL_SUFFIX
        logger.info("Getting SAML request from url: %s", saml_controller_url)
        resp = controller_session.get(saml_controller_url,
                                      allow_redirects=True)
        if resp.status_code != 200:
            logger.error('Status Code %s msg %s' % (
                resp.status_code, resp.text))
            raise APIError('Status Code %s msg %s' % (
                resp.status_code, resp.text), resp)
        # Getting IDP session
        idp_session = requests.Session()
        saml_request_match = re.search(OneloginSAMLApiSession.saml_request_regex, resp.text,
                                       re.M | re.S)
        if not saml_request_match:
            logger.error("SAML request not generated by controller.")
            raise APIError("SAML request not generated by controller.")
        saml_request = saml_request_match.group(1)
        relay_state = re.search(OneloginSAMLApiSession.request_relay_state_regex, resp.text,
                                re.M | re.S).group(1)
        assertion_url = re.search(OneloginSAMLApiSession.request_assertion_url_regex, resp.text,
                                  re.M | re.S).group(1)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        saml_data = urllib.urlencode({
            'SAMLRequest': saml_request,
            'RelayState': relay_state})
        if self.idp_cookies:
            logger.info("Controller url %s generated SAML request is being "
                        "sent to IDP with existing IDP cookies.",
                        saml_controller_url)
            idp_resp = idp_session.post(assertion_url, headers=headers,
                                        data=saml_data, allow_redirects=False,
                                        cookies=self.idp_cookies)
        else:
            logger.info("Controller url %s generated SAML request is being "
                        "sent to IDP.", saml_controller_url)
            idp_resp = idp_session.post(assertion_url, headers=headers,
                                        data=saml_data,
                                        allow_redirects=False)
        if resp.status_code not in (200, 301, 302):
            logger.error('Status Code %s msg %s' % (
                resp.status_code, resp.text))
            raise APIError('Status Code %s msg %s' % (
                resp.status_code, resp.text), resp)
        if "SAMLResponse" not in idp_resp.text:
            redirect_url = idp_resp.headers['Location']
            idp_resp = idp_session.get(redirect_url,
                                       allow_redirects=False)
            if resp.status_code not in (200, 301, 302):
                logger.error('Status Code %s msg %s' % (
                    resp.status_code, resp.text))
                raise APIError('Status Code %s msg %s' % (
                    resp.status_code, resp.text), resp)
            query_string = idp_resp.headers['Location'].split('=')[1]
            data = {"return": query_string}
            json_data = json.dumps(data)
            headers = {'content-type': 'application/json'}
            parsed_uri = urlparse.urlparse(assertion_url)
            # This needs to be modified for other IDPs.
            auth_url = "{}://{}/access/auth".format(parsed_uri.scheme,
                                                    parsed_uri.netloc)
            resp = idp_session.post(auth_url, headers=headers,
                                    data=json_data)
            if resp.status_code in [401, 403]:
                logger.error('Status Code %s msg Invalid SAML credentials %s'
                             % (resp.status_code, resp.text))
                raise APIError('Status Code %s msg Invalid SAML credentials %s'
                               % (resp.status_code, resp.text), resp)
            elif resp.status_code != 200:
                logger.error('Status Code %s msg %s' % (
                    resp.status_code, resp.text))
                raise APIError('Status Code %s msg %s' % (
                    resp.status_code, resp.text), resp)
            # credentials payload for given IDP
            credentials_tuple = [('username', 'login',
                                  username),
                                 ('password', 'password',
                                  password)]
            for state in credentials_tuple:
                bearer = "Bearer " + resp.text.split('jwt":"')[1][:-3]
                headers = {'content-type': 'application/json',
                           'authorization': bearer}
                user_data = {'state': state[0],
                             'payload': {state[1]: state[2]}}
                json_data = json.dumps(user_data)
                resp = idp_session.put(auth_url, headers=headers,
                                       data=json_data)
                if resp.status_code in [401, 403]:
                    logger.error('Status Code %s msg Invalid SAML credentials %s'
                                 % (resp.status_code, resp.text))
                    raise APIError('Status Code %s msg Invalid SAML credentials %s'
                                   % (resp.status_code, resp.text), resp)
                elif resp.status_code != 200:
                    logger.error('Status Code %s msg %s' % (
                        resp.status_code, resp.text))
                    raise APIError('Status Code %s msg %s' % (
                        resp.status_code, resp.text), resp)
            data = json.loads(resp.text)
            try:
                token = data["request"]["params"]["saml_request_params_token"]
            except KeyError:
                raise APIError("Couldn't complete "
                               "authentication with IDP")
            url = data["request"]["uri"]
            params = {'saml_request_params_token': token}
            resp = idp_session.get(url, params=params)
            if resp.status_code != 200:
                logger.error('Status Code %s msg %s' % (
                    resp.status_code, resp.text))
                raise APIError('Status Code %s msg %s' % (
                    resp.status_code, resp.text), resp)
        return controller_session, resp

    def authenticate_session(self):
        """
        Performs SAML authentication with Avi controller and IDPs.
        Stores session cookies and sets header parameters.
        """

        username = self.avi_credentials.username
        if self.avi_credentials.password:
            password = self.avi_credentials.password
        else:
            raise APIError("No user password provided")
        logger.debug('authenticating user %s prefix %s',
                     self.avi_credentials.username, self.prefix)
        self.cookies.clear()
        try:
            # Assert SAML response
            controller_session, resp = self.saml_assertion(username, password)
            content = resp.text
            saml_response_match = re.search(OneloginSAMLApiSession.saml_response_regex, content,
                                            re.M | re.S)
            saml_response = saml_response_match.group(1)
            relay_state = re.search(OneloginSAMLApiSession.response_relay_state_regex, content, re.M |
                                    re.S).group(1)
            assertion_url = re.search(OneloginSAMLApiSession.response_assertion_url_regex, content, re.M |
                                      re.S).group(1)
            saml_data = urllib.urlencode([
                ('SAMLResponse', saml_response),
                ('RelayState', relay_state)])
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            rsp = controller_session.post(assertion_url,
                                          headers=headers,
                                          data=saml_data)
            if rsp.status_code == 200:
                self.num_session_retries = 0
                self.remote_api_version = \
                    rsp.headers.get('AVI_API_VERSION', {})
                self.headers.update(self.user_hdrs)
                if rsp.cookies and 'csrftoken' in rsp.cookies:
                    sessionDict[self.key] = {
                        'csrftoken': rsp.cookies['csrftoken'],
                        'session_id': rsp.cookies['sessionid'],
                        'last_used': datetime.utcnow(),
                        'api': self,
                        'connected': True
                    }
                logger.debug("authentication success for user %s",
                             self.avi_credentials.username)
                return
            # Check for bad request and invalid credentials response code
            elif rsp.status_code in [401, 403]:
                logger.error('Status Code %s msg %s' % (
                    rsp.status_code, rsp.text))
                err = APIError('Status Code %s msg %s' % (
                    rsp.status_code, rsp.text), rsp)
            else:
                logger.error("Error status code %s msg %s", rsp.status_code,
                             rsp.text)
                err = APIError('Status Code %s msg %s' % (
                    rsp.status_code, rsp.text), rsp)
        except (ConnectionError, SSLError, ChunkedEncodingError) as e:
            if not self.retry_conxn_errors:
                raise
            logger.warning('Connection error retrying %s', e)
            err = e
        # comes here only if there was either exception or login was not
        # successful
        if self.retry_wait_time:
            time.sleep(self.retry_wait_time)
        self.num_session_retries += 1
        if self.num_session_retries > self.max_session_retries:
            self.num_session_retries = 0
            logger.error("Giving up after %d retries connection failure %s" % (
                self.max_session_retries, True))
            raise err
        self.authenticate_session()
        return


class OktaSAMLApiSession(ApiSession):
    """
    Extends the ApiSession session class to provide helper
    utilities to work with Avi Controller and IDP for SAML assertion and
    authentication, api massaging, etc
    """

    SAML_URL_SUFFIX = "/sso/login"
    # Request RegX
    saml_request_regex = r'<input type=\"hidden\" ' \
                         r'name=\"SAMLRequest\" value=\"(.*?)\"'
    request_relay_state_regex = r'<input type=\"hidden\" ' \
                                r'name=\"RelayState\" value=\"(.*?)\"'
    request_assertion_url_regex = r'<form method=\"post\" action=\"(.*?)\">'
    # Response RegX
    saml_response_regex = r'<input name=\"SAMLResponse\" ' \
                          r'type=\"hidden\" value=\"(.*?)\"'
    response_relay_state_regex = r'<input name=\"RelayState\" ' \
                                 r'type=\"hidden\" value=\"(.*?)\"'
    response_assertion_url_regex = r'<form id=\"appForm\" ' \
                                   r'action=\"(.*?)\" method=\"post\">'

    def __init__(self, controller=None, username=None, password=None,
                 token=None, tenant=None, tenant_uuid=None, verify=False,
                 port=None, timeout=60, api_version=None,
                 retry_conxn_errors=True, data_log=False,
                 avi_credentials=None, session_id=None, csrftoken=None,
                 lazy_authentication=False, max_api_retries=None,
                 idp_cookies=None):
        """
        This extends ApiSession class and overrides authentication method
        for SMAL authentication.

        :param controller: Controller IP
        :param username: IDP username
        :param password: IDP password
        :param token: Controller token
        :param tenant: Overrides the tenant used during session creation
        :param tenant_uuid: Overrides the tenant or tenant_uuid during session
            creation
        :param verify: Boolean flag for SSL verification of url
        :param port: Controller SSO port
        :param timeout: Timeout for API calls; Default value is 60 seconds
        :param api_version: Overrides x-avi-header in request header during
            session creation
        :param retry_conxn_errors: Retry on connection errors
        :param data_log: Data log
        :param avi_credentials: avi_credential object
        :param session_id: Session ID
        :param csrftoken: CSRF Token
        :param lazy_authentication: Lazy_authentication for controller.
        :param max_api_retries: Maximum API retires
        :param idp_cookies: IDP cookies if want to use existing IDP session
        """

        self.idp_cookies = idp_cookies
        super(OktaSAMLApiSession, self).__init__(
            controller, username, password, token,
            tenant, tenant_uuid, verify,
            port, timeout, api_version,
            retry_conxn_errors, data_log,
            avi_credentials, session_id, csrftoken,
            lazy_authentication, max_api_retries)
        return

    def saml_assertion(self, username, password):
        """
        Perform SAML request from controller to IDPs.
        Establish session with controller and IDP.
        Assert SAML request into the reqeust.
        Get the controller session and IDP session.

        :param username: IDP Username
        :param password: IDP Password
        :return: controller session and IDP response
        """

        # Getting controller session
        controller_session = requests.Session()
        controller_session.verify = False
        saml_controller_url = self.prefix + self.SAML_URL_SUFFIX
        logger.info("Getting SAML request from url: %s", saml_controller_url)
        resp = controller_session.get(saml_controller_url,
                                      allow_redirects=True)
        if resp.status_code != 200:
            logger.error('Status Code %s msg %s' % (
                resp.status_code, resp.text))
            raise APIError('Status Code %s msg %s' % (
                resp.status_code, resp.text), resp)
        saml_request_match = re.search(OktaSAMLApiSession.saml_request_regex, resp.text,
                                       re.M | re.S)
        if not saml_request_match:
            logger.error("SAML request not generated by controller.")
            raise APIError("SAML request not generated by controller.")
        saml_request = saml_request_match.group(1)
        relay_state = re.search(OktaSAMLApiSession.request_relay_state_regex, resp.text,
                                re.M | re.S).group(1)
        assertion_url = re.search(OktaSAMLApiSession.request_assertion_url_regex, resp.text,
                                  re.M | re.S).group(1)

        idp_session = requests.Session()
        idp_session.verify = False
        saml_data = urllib.parse.urlencode({
            'SAMLRequest': saml_request,
            'RelayState': relay_state})
        parsed_uri = urllib.parse.urlparse(assertion_url)
        base_url = "{}://{}".format(parsed_uri.scheme, parsed_uri.netloc)
        if self.idp_cookies:
            logger.info("Controller url %s generated SAML request is being "
                        "sent to IDP with existing IDP cookies.",
                        saml_controller_url)
            resp = idp_session.get(assertion_url, allow_redirects=False,
                                   cookies=self.idp_cookies)
        else:
            logger.info("Controller url %s generated SAML request is being "
                        "sent to IDP.", saml_controller_url)
            resp = idp_session.get(assertion_url, allow_redirects=False)
        if resp.status_code not in (200, 301, 302):
            logger.error('Status Code %s msg %s' % (
                resp.status_code, resp.text))
            raise APIError('Status Code %s msg %s' % (
                resp.status_code, resp.text), resp)
        if "SAMLResponse" not in resp.text:
            user_data = {"username": username,
                         "options": {"warnBeforePasswordExpired": True,
                                     "multiOptionalFactorEnroll": True},
                         "password": password}
            json_data = json.dumps(user_data)
            headers = {'content-type': 'application/json'}
            resp = idp_session.post(base_url + "/api/v1/authn",
                                    headers=headers,
                                    data=json_data)
            if resp.status_code in [401, 403]:
                logger.error('Status Code %s msg Invalid SAML credentials %s'
                             % (resp.status_code, resp.text))
                raise APIError('Status Code %s msg Invalid SAML credentials %s'
                               % (resp.status_code, resp.text), resp)
            elif resp.status_code != 200:
                logger.error('Status Code %s msg %s' % (
                    resp.status_code, resp.text))
                raise APIError('Status Code %s msg %s' % (
                    resp.status_code, resp.text), resp)
            data = json.loads(resp.text)
            try:
                token = data["sessionToken"]
            except KeyError:
                raise APIError("Couldn't complete authentication with IDP")
            new_url = base_url + "/login/sessionCookieRedirect"
            redirect_url = "{}?{}".format(assertion_url, saml_data)
            params = {'checkAccountSetupComplete': 'true',
                      'token': token,
                      'redirectUrl': redirect_url}
            resp = idp_session.get(new_url, params=params,
                                   allow_redirects=True)
            if resp.status_code not in (200, 301, 302):
                logger.error('Status Code %s msg %s' % (
                    resp.status_code, resp.text))
                raise APIError('Status Code %s msg %s' % (
                    resp.status_code, resp.text), resp)
        return controller_session, resp

    def authenticate_session(self):
        """
        Performs SAML authentication with Avi controller and IDPs.
        Stores session cookies and sets header parameters.
        """

        username = self.avi_credentials.username
        if self.avi_credentials.password:
            password = self.avi_credentials.password
        else:
            raise APIError("No user password provided")
        logger.debug('authenticating user %s prefix %s',
                     self.avi_credentials.username, self.prefix)
        self.cookies.clear()
        try:
            # Assert SAML response
            controller_session, resp = self.saml_assertion(username, password)
            content = resp.text
            saml_response_match = re.search(OktaSAMLApiSession.saml_response_regex,
                                            content, re.M | re.S)
            saml_response = saml_response_match.group(1)
            assertion_url = re.search(OktaSAMLApiSession.response_assertion_url_regex, content,
                                      re.M | re.S |
                                      re.IGNORECASE).group(1)
            relay_state = re.search(OktaSAMLApiSession.response_relay_state_regex, content,
                                    re.M | re.S).group(1)
            from HTMLParser import HTMLParser
            parser = HTMLParser()
            assertion_url = parser.unescape(assertion_url)
            saml_response = parser.unescape(saml_response)
            saml_data = urllib.urlencode([
                ('SAMLResponse', saml_response),
                ('RelayState', relay_state)])
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            rsp = controller_session.post(assertion_url,
                                          headers=headers,
                                          data=saml_data,
                                          allow_redirects=True)
            if rsp.status_code == 200:
                self.num_session_retries = 0
                self.remote_api_version = \
                    rsp.headers.get('AVI_API_VERSION', {})
                self.headers.update(self.user_hdrs)
                if rsp.cookies and 'csrftoken' in rsp.cookies:
                    sessionDict[self.key] = {
                        'csrftoken': rsp.cookies['csrftoken'],
                        'session_id': rsp.cookies['sessionid'],
                        'last_used': datetime.utcnow(),
                        'api': self,
                        'connected': True
                    }
                logger.debug("authentication success for user %s",
                             self.avi_credentials.username)
                return
            # Check for bad request and invalid credentials response code
            elif rsp.status_code in [401, 403]:
                logger.error('Status Code %s msg %s' % (
                    rsp.status_code, rsp.text))
                err = APIError('Status Code %s msg %s' % (
                    rsp.status_code, rsp.text), rsp)
                raise err
            else:
                logger.error("Error status code %s msg %s", rsp.status_code,
                             rsp.text)
                err = APIError('Status Code %s msg %s' % (
                    rsp.status_code, rsp.text), rsp)
        except (ConnectionError, SSLError, ChunkedEncodingError) as e:
            if not self.retry_conxn_errors:
                raise
            logger.warning('Connection error retrying %s', e)
            err = e
        # Comes here only if there was either exception or login was not
        # successful
        if self.retry_wait_time:
            time.sleep(self.retry_wait_time)
        self.num_session_retries += 1
        if self.num_session_retries > self.max_session_retries:
            self.num_session_retries = 0
            logger.error("Giving up after %d retries connection failure %s" % (
                self.max_session_retries, True))
            raise err
        self.authenticate_session()
        return
