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
import io.swagger.v3.oas.annotations.media.Schema;
/**
 * FeProxyRoutePublishConfig
 */

@javax.annotation.Generated(value = "io.swagger.codegen.v3.generators.java.JavaClientCodegen", date = "2020-03-12T12:27:26.755+05:30[Asia/Kolkata]")
public class FeProxyRoutePublishConfig {
  @JsonProperty("mode")
  private String mode = "FE_PROXY_ROUTE_PUBLISH_NONE";

  @JsonProperty("publisher_port")
  private Integer publisherPort = 80;

  @JsonProperty("subnet")
  private Integer subnet = 32;

  @JsonProperty("token")
  private String token = null;

  public FeProxyRoutePublishConfig mode(String mode) {
    this.mode = mode;
    return this;
  }

   /**
   * Publish ECMP route to upstream router for VIP. Enum options - FE_PROXY_ROUTE_PUBLISH_NONE, FE_PROXY_ROUTE_PUBLISH_QUAGGA_WEBAPP.
   * @return mode
  **/
  @Schema(description = "Publish ECMP route to upstream router for VIP. Enum options - FE_PROXY_ROUTE_PUBLISH_NONE, FE_PROXY_ROUTE_PUBLISH_QUAGGA_WEBAPP.")
  public String getMode() {
    return mode;
  }

  public void setMode(String mode) {
    this.mode = mode;
  }

  public FeProxyRoutePublishConfig publisherPort(Integer publisherPort) {
    this.publisherPort = publisherPort;
    return this;
  }

   /**
   * Listener port for publisher.
   * @return publisherPort
  **/
  @Schema(description = "Listener port for publisher.")
  public Integer getPublisherPort() {
    return publisherPort;
  }

  public void setPublisherPort(Integer publisherPort) {
    this.publisherPort = publisherPort;
  }

  public FeProxyRoutePublishConfig subnet(Integer subnet) {
    this.subnet = subnet;
    return this;
  }

   /**
   * Subnet for publisher.
   * @return subnet
  **/
  @Schema(description = "Subnet for publisher.")
  public Integer getSubnet() {
    return subnet;
  }

  public void setSubnet(Integer subnet) {
    this.subnet = subnet;
  }

  public FeProxyRoutePublishConfig token(String token) {
    this.token = token;
    return this;
  }

   /**
   * Token for tracking changes.
   * @return token
  **/
  @Schema(description = "Token for tracking changes.")
  public String getToken() {
    return token;
  }

  public void setToken(String token) {
    this.token = token;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    FeProxyRoutePublishConfig feProxyRoutePublishConfig = (FeProxyRoutePublishConfig) o;
    return Objects.equals(this.mode, feProxyRoutePublishConfig.mode) &&
        Objects.equals(this.publisherPort, feProxyRoutePublishConfig.publisherPort) &&
        Objects.equals(this.subnet, feProxyRoutePublishConfig.subnet) &&
        Objects.equals(this.token, feProxyRoutePublishConfig.token);
  }

  @Override
  public int hashCode() {
    return Objects.hash(mode, publisherPort, subnet, token);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class FeProxyRoutePublishConfig {\n");
    
    sb.append("    mode: ").append(toIndentedString(mode)).append("\n");
    sb.append("    publisherPort: ").append(toIndentedString(publisherPort)).append("\n");
    sb.append("    subnet: ").append(toIndentedString(subnet)).append("\n");
    sb.append("    token: ").append(toIndentedString(token)).append("\n");
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