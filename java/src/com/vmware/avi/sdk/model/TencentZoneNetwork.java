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
 * TencentZoneNetwork
 */

@javax.annotation.Generated(value = "io.swagger.codegen.v3.generators.java.JavaClientCodegen", date = "2020-03-12T12:27:26.755+05:30[Asia/Kolkata]")
public class TencentZoneNetwork {
  @JsonProperty("availability_zone")
  private String availabilityZone = null;

  @JsonProperty("usable_subnet_id")
  private String usableSubnetId = null;

  public TencentZoneNetwork availabilityZone(String availabilityZone) {
    this.availabilityZone = availabilityZone;
    return this;
  }

   /**
   * Availability zone. Field introduced in 18.2.3.
   * @return availabilityZone
  **/
  @Schema(required = true, description = "Availability zone. Field introduced in 18.2.3.")
  public String getAvailabilityZone() {
    return availabilityZone;
  }

  public void setAvailabilityZone(String availabilityZone) {
    this.availabilityZone = availabilityZone;
  }

  public TencentZoneNetwork usableSubnetId(String usableSubnetId) {
    this.usableSubnetId = usableSubnetId;
    return this;
  }

   /**
   * Usable networks for Virtual IP. If VirtualService does not specify a network and auto_allocate_ip is set, then the first available network from this list will be chosen for IP allocation. Field introduced in 18.2.3.
   * @return usableSubnetId
  **/
  @Schema(required = true, description = "Usable networks for Virtual IP. If VirtualService does not specify a network and auto_allocate_ip is set, then the first available network from this list will be chosen for IP allocation. Field introduced in 18.2.3.")
  public String getUsableSubnetId() {
    return usableSubnetId;
  }

  public void setUsableSubnetId(String usableSubnetId) {
    this.usableSubnetId = usableSubnetId;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    TencentZoneNetwork tencentZoneNetwork = (TencentZoneNetwork) o;
    return Objects.equals(this.availabilityZone, tencentZoneNetwork.availabilityZone) &&
        Objects.equals(this.usableSubnetId, tencentZoneNetwork.usableSubnetId);
  }

  @Override
  public int hashCode() {
    return Objects.hash(availabilityZone, usableSubnetId);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class TencentZoneNetwork {\n");
    
    sb.append("    availabilityZone: ").append(toIndentedString(availabilityZone)).append("\n");
    sb.append("    usableSubnetId: ").append(toIndentedString(usableSubnetId)).append("\n");
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
