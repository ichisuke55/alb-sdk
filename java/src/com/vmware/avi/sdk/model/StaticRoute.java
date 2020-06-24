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
import com.vmware.avi.sdk.model.IpAddr;
import com.vmware.avi.sdk.model.IpAddrPrefix;
import io.swagger.v3.oas.annotations.media.Schema;
/**
 * StaticRoute
 */

@javax.annotation.Generated(value = "io.swagger.codegen.v3.generators.java.JavaClientCodegen", date = "2020-03-12T12:27:26.755+05:30[Asia/Kolkata]")
public class StaticRoute {
  @JsonProperty("disable_gateway_monitor")
  private Boolean disableGatewayMonitor = null;

  @JsonProperty("if_name")
  private String ifName = null;

  @JsonProperty("next_hop")
  private IpAddr nextHop = null;

  @JsonProperty("prefix")
  private IpAddrPrefix prefix = null;

  @JsonProperty("route_id")
  private String routeId = null;

  public StaticRoute disableGatewayMonitor(Boolean disableGatewayMonitor) {
    this.disableGatewayMonitor = disableGatewayMonitor;
    return this;
  }

   /**
   * Disable the gateway monitor for default gateway. They are monitored by default. Field introduced in 17.1.1.
   * @return disableGatewayMonitor
  **/
  @Schema(description = "Disable the gateway monitor for default gateway. They are monitored by default. Field introduced in 17.1.1.")
  public Boolean isDisableGatewayMonitor() {
    return disableGatewayMonitor;
  }

  public void setDisableGatewayMonitor(Boolean disableGatewayMonitor) {
    this.disableGatewayMonitor = disableGatewayMonitor;
  }

  public StaticRoute ifName(String ifName) {
    this.ifName = ifName;
    return this;
  }

   /**
   * if_name of StaticRoute.
   * @return ifName
  **/
  @Schema(description = "if_name of StaticRoute.")
  public String getIfName() {
    return ifName;
  }

  public void setIfName(String ifName) {
    this.ifName = ifName;
  }

  public StaticRoute nextHop(IpAddr nextHop) {
    this.nextHop = nextHop;
    return this;
  }

   /**
   * Get nextHop
   * @return nextHop
  **/
  @Schema(required = true, description = "")
  public IpAddr getNextHop() {
    return nextHop;
  }

  public void setNextHop(IpAddr nextHop) {
    this.nextHop = nextHop;
  }

  public StaticRoute prefix(IpAddrPrefix prefix) {
    this.prefix = prefix;
    return this;
  }

   /**
   * Get prefix
   * @return prefix
  **/
  @Schema(required = true, description = "")
  public IpAddrPrefix getPrefix() {
    return prefix;
  }

  public void setPrefix(IpAddrPrefix prefix) {
    this.prefix = prefix;
  }

  public StaticRoute routeId(String routeId) {
    this.routeId = routeId;
    return this;
  }

   /**
   * route_id of StaticRoute.
   * @return routeId
  **/
  @Schema(required = true, description = "route_id of StaticRoute.")
  public String getRouteId() {
    return routeId;
  }

  public void setRouteId(String routeId) {
    this.routeId = routeId;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    StaticRoute staticRoute = (StaticRoute) o;
    return Objects.equals(this.disableGatewayMonitor, staticRoute.disableGatewayMonitor) &&
        Objects.equals(this.ifName, staticRoute.ifName) &&
        Objects.equals(this.nextHop, staticRoute.nextHop) &&
        Objects.equals(this.prefix, staticRoute.prefix) &&
        Objects.equals(this.routeId, staticRoute.routeId);
  }

  @Override
  public int hashCode() {
    return Objects.hash(disableGatewayMonitor, ifName, nextHop, prefix, routeId);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class StaticRoute {\n");
    
    sb.append("    disableGatewayMonitor: ").append(toIndentedString(disableGatewayMonitor)).append("\n");
    sb.append("    ifName: ").append(toIndentedString(ifName)).append("\n");
    sb.append("    nextHop: ").append(toIndentedString(nextHop)).append("\n");
    sb.append("    prefix: ").append(toIndentedString(prefix)).append("\n");
    sb.append("    routeId: ").append(toIndentedString(routeId)).append("\n");
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
