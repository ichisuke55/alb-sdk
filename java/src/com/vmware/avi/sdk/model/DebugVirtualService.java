/*
 * Avi avi_global_spec Object API
 * No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)
 *
 * OpenAPI spec version: 20.1.1
 * Contact: support@avinetworks.com
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */

package com.vmware.avi.sdk.model;

import java.util.Objects;
import java.util.Arrays;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import com.vmware.avi.sdk.model.CaptureFilters;
import com.vmware.avi.sdk.model.DebugDnsOptions;
import com.vmware.avi.sdk.model.DebugIpAddr;
import com.vmware.avi.sdk.model.DebugVirtualServiceCapture;
import com.vmware.avi.sdk.model.DebugVirtualServiceSeParams;
import com.vmware.avi.sdk.model.DebugVsDataplane;
import io.swagger.v3.oas.annotations.media.Schema;
import java.util.ArrayList;
import java.util.List;
/**
 * DebugVirtualService
 */

@javax.annotation.Generated(value = "io.swagger.codegen.v3.generators.java.JavaClientCodegen", date = "2020-03-12T12:27:26.755+05:30[Asia/Kolkata]")
public class DebugVirtualService {
  @JsonProperty("_last_modified")
  private String _lastModified = null;

  @JsonProperty("capture")
  private Boolean capture = null;

  @JsonProperty("capture_filters")
  private CaptureFilters captureFilters = null;

  @JsonProperty("capture_params")
  private DebugVirtualServiceCapture captureParams = null;

  @JsonProperty("cloud_ref")
  private String cloudRef = null;

  @JsonProperty("debug_hm")
  private String debugHm = "DEBUG_VS_HM_NONE";

  @JsonProperty("debug_ip")
  private DebugIpAddr debugIp = null;

  @JsonProperty("dns_options")
  private DebugDnsOptions dnsOptions = null;

  @JsonProperty("flags")
  private List<DebugVsDataplane> flags = null;

  @JsonProperty("name")
  private String name = null;

  @JsonProperty("resync_flows")
  private Boolean resyncFlows = null;

  @JsonProperty("se_params")
  private DebugVirtualServiceSeParams seParams = null;

  @JsonProperty("tenant_ref")
  private String tenantRef = null;

  @JsonProperty("url")
  private String url = null;

  @JsonProperty("uuid")
  private String uuid = null;

   /**
   * UNIX time since epoch in microseconds. Units(MICROSECONDS).
   * @return _lastModified
  **/
  @Schema(description = "UNIX time since epoch in microseconds. Units(MICROSECONDS).")
  public String getLastModified() {
    return _lastModified;
  }

  public DebugVirtualService capture(Boolean capture) {
    this.capture = capture;
    return this;
  }

   /**
   * Placeholder for description of property capture of obj type DebugVirtualService field type str  type boolean
   * @return capture
  **/
  @Schema(description = "Placeholder for description of property capture of obj type DebugVirtualService field type str  type boolean")
  public Boolean isCapture() {
    return capture;
  }

  public void setCapture(Boolean capture) {
    this.capture = capture;
  }

  public DebugVirtualService captureFilters(CaptureFilters captureFilters) {
    this.captureFilters = captureFilters;
    return this;
  }

   /**
   * Get captureFilters
   * @return captureFilters
  **/
  @Schema(description = "")
  public CaptureFilters getCaptureFilters() {
    return captureFilters;
  }

  public void setCaptureFilters(CaptureFilters captureFilters) {
    this.captureFilters = captureFilters;
  }

  public DebugVirtualService captureParams(DebugVirtualServiceCapture captureParams) {
    this.captureParams = captureParams;
    return this;
  }

   /**
   * Get captureParams
   * @return captureParams
  **/
  @Schema(description = "")
  public DebugVirtualServiceCapture getCaptureParams() {
    return captureParams;
  }

  public void setCaptureParams(DebugVirtualServiceCapture captureParams) {
    this.captureParams = captureParams;
  }

  public DebugVirtualService cloudRef(String cloudRef) {
    this.cloudRef = cloudRef;
    return this;
  }

   /**
   *  It is a reference to an object of type Cloud.
   * @return cloudRef
  **/
  @Schema(description = " It is a reference to an object of type Cloud.")
  public String getCloudRef() {
    return cloudRef;
  }

  public void setCloudRef(String cloudRef) {
    this.cloudRef = cloudRef;
  }

  public DebugVirtualService debugHm(String debugHm) {
    this.debugHm = debugHm;
    return this;
  }

   /**
   * This option controls the capture of Health Monitor flows. Enum options - DEBUG_VS_HM_NONE, DEBUG_VS_HM_ONLY, DEBUG_VS_HM_INCLUDE.
   * @return debugHm
  **/
  @Schema(description = "This option controls the capture of Health Monitor flows. Enum options - DEBUG_VS_HM_NONE, DEBUG_VS_HM_ONLY, DEBUG_VS_HM_INCLUDE.")
  public String getDebugHm() {
    return debugHm;
  }

  public void setDebugHm(String debugHm) {
    this.debugHm = debugHm;
  }

  public DebugVirtualService debugIp(DebugIpAddr debugIp) {
    this.debugIp = debugIp;
    return this;
  }

   /**
   * Get debugIp
   * @return debugIp
  **/
  @Schema(description = "")
  public DebugIpAddr getDebugIp() {
    return debugIp;
  }

  public void setDebugIp(DebugIpAddr debugIp) {
    this.debugIp = debugIp;
  }

  public DebugVirtualService dnsOptions(DebugDnsOptions dnsOptions) {
    this.dnsOptions = dnsOptions;
    return this;
  }

   /**
   * Get dnsOptions
   * @return dnsOptions
  **/
  @Schema(description = "")
  public DebugDnsOptions getDnsOptions() {
    return dnsOptions;
  }

  public void setDnsOptions(DebugDnsOptions dnsOptions) {
    this.dnsOptions = dnsOptions;
  }

  public DebugVirtualService flags(List<DebugVsDataplane> flags) {
    this.flags = flags;
    return this;
  }

  public DebugVirtualService addFlagsItem(DebugVsDataplane flagsItem) {
    if (this.flags == null) {
      this.flags = new ArrayList<DebugVsDataplane>();
    }
    this.flags.add(flagsItem);
    return this;
  }

   /**
   * Placeholder for description of property flags of obj type DebugVirtualService field type str  type object
   * @return flags
  **/
  @Schema(description = "Placeholder for description of property flags of obj type DebugVirtualService field type str  type object")
  public List<DebugVsDataplane> getFlags() {
    return flags;
  }

  public void setFlags(List<DebugVsDataplane> flags) {
    this.flags = flags;
  }

  public DebugVirtualService name(String name) {
    this.name = name;
    return this;
  }

   /**
   * Name of the object.
   * @return name
  **/
  @Schema(required = true, description = "Name of the object.")
  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public DebugVirtualService resyncFlows(Boolean resyncFlows) {
    this.resyncFlows = resyncFlows;
    return this;
  }

   /**
   * This option re-synchronizes flows between Active-Standby service engines for all the virtual services placed on them. It should be used with caution because as it can cause a flood between Active-Standby. Field introduced in 18.1.3,18.2.1.
   * @return resyncFlows
  **/
  @Schema(description = "This option re-synchronizes flows between Active-Standby service engines for all the virtual services placed on them. It should be used with caution because as it can cause a flood between Active-Standby. Field introduced in 18.1.3,18.2.1.")
  public Boolean isResyncFlows() {
    return resyncFlows;
  }

  public void setResyncFlows(Boolean resyncFlows) {
    this.resyncFlows = resyncFlows;
  }

  public DebugVirtualService seParams(DebugVirtualServiceSeParams seParams) {
    this.seParams = seParams;
    return this;
  }

   /**
   * Get seParams
   * @return seParams
  **/
  @Schema(description = "")
  public DebugVirtualServiceSeParams getSeParams() {
    return seParams;
  }

  public void setSeParams(DebugVirtualServiceSeParams seParams) {
    this.seParams = seParams;
  }

  public DebugVirtualService tenantRef(String tenantRef) {
    this.tenantRef = tenantRef;
    return this;
  }

   /**
   *  It is a reference to an object of type Tenant.
   * @return tenantRef
  **/
  @Schema(description = " It is a reference to an object of type Tenant.")
  public String getTenantRef() {
    return tenantRef;
  }

  public void setTenantRef(String tenantRef) {
    this.tenantRef = tenantRef;
  }

   /**
   * url
   * @return url
  **/
  @Schema(description = "url")
  public String getUrl() {
    return url;
  }

  public DebugVirtualService uuid(String uuid) {
    this.uuid = uuid;
    return this;
  }

   /**
   * Unique object identifier of the object.
   * @return uuid
  **/
  @Schema(description = "Unique object identifier of the object.")
  public String getUuid() {
    return uuid;
  }

  public void setUuid(String uuid) {
    this.uuid = uuid;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    DebugVirtualService debugVirtualService = (DebugVirtualService) o;
    return Objects.equals(this._lastModified, debugVirtualService._lastModified) &&
        Objects.equals(this.capture, debugVirtualService.capture) &&
        Objects.equals(this.captureFilters, debugVirtualService.captureFilters) &&
        Objects.equals(this.captureParams, debugVirtualService.captureParams) &&
        Objects.equals(this.cloudRef, debugVirtualService.cloudRef) &&
        Objects.equals(this.debugHm, debugVirtualService.debugHm) &&
        Objects.equals(this.debugIp, debugVirtualService.debugIp) &&
        Objects.equals(this.dnsOptions, debugVirtualService.dnsOptions) &&
        Objects.equals(this.flags, debugVirtualService.flags) &&
        Objects.equals(this.name, debugVirtualService.name) &&
        Objects.equals(this.resyncFlows, debugVirtualService.resyncFlows) &&
        Objects.equals(this.seParams, debugVirtualService.seParams) &&
        Objects.equals(this.tenantRef, debugVirtualService.tenantRef) &&
        Objects.equals(this.url, debugVirtualService.url) &&
        Objects.equals(this.uuid, debugVirtualService.uuid);
  }

  @Override
  public int hashCode() {
    return Objects.hash(_lastModified, capture, captureFilters, captureParams, cloudRef, debugHm, debugIp, dnsOptions, flags, name, resyncFlows, seParams, tenantRef, url, uuid);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class DebugVirtualService {\n");
    
    sb.append("    _lastModified: ").append(toIndentedString(_lastModified)).append("\n");
    sb.append("    capture: ").append(toIndentedString(capture)).append("\n");
    sb.append("    captureFilters: ").append(toIndentedString(captureFilters)).append("\n");
    sb.append("    captureParams: ").append(toIndentedString(captureParams)).append("\n");
    sb.append("    cloudRef: ").append(toIndentedString(cloudRef)).append("\n");
    sb.append("    debugHm: ").append(toIndentedString(debugHm)).append("\n");
    sb.append("    debugIp: ").append(toIndentedString(debugIp)).append("\n");
    sb.append("    dnsOptions: ").append(toIndentedString(dnsOptions)).append("\n");
    sb.append("    flags: ").append(toIndentedString(flags)).append("\n");
    sb.append("    name: ").append(toIndentedString(name)).append("\n");
    sb.append("    resyncFlows: ").append(toIndentedString(resyncFlows)).append("\n");
    sb.append("    seParams: ").append(toIndentedString(seParams)).append("\n");
    sb.append("    tenantRef: ").append(toIndentedString(tenantRef)).append("\n");
    sb.append("    url: ").append(toIndentedString(url)).append("\n");
    sb.append("    uuid: ").append(toIndentedString(uuid)).append("\n");
    sb.append("}");
    return sb.toString();
  }

  /**
   * Convert the given object to string with each line indented by 4 spaces
   * (except the first line).
   */
  private String toIndentedString(java.lang.Object o) {
    if (o == null) {
      return "null";
    }
    return o.toString().replace("\n", "\n    ");
  }

}