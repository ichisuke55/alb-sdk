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
import com.vmware.avi.sdk.model.GeoLocation;
import io.swagger.v3.oas.annotations.media.Schema;
/**
 * GslbGeoLocation
 */

@javax.annotation.Generated(value = "io.swagger.codegen.v3.generators.java.JavaClientCodegen", date = "2020-03-12T12:27:26.755+05:30[Asia/Kolkata]")
public class GslbGeoLocation {
  @JsonProperty("location")
  private GeoLocation location = null;

  @JsonProperty("source")
  private String source = null;

  public GslbGeoLocation location(GeoLocation location) {
    this.location = location;
    return this;
  }

   /**
   * Get location
   * @return location
  **/
  @Schema(description = "")
  public GeoLocation getLocation() {
    return location;
  }

  public void setLocation(GeoLocation location) {
    this.location = location;
  }

  public GslbGeoLocation source(String source) {
    this.source = source;
    return this;
  }

   /**
   * This field describes the source of the GeoLocation. . Enum options - GSLB_LOCATION_SRC_USER_CONFIGURED, GSLB_LOCATION_SRC_INHERIT_FROM_SITE, GSLB_LOCATION_SRC_FROM_GEODB. Field introduced in 17.1.1.
   * @return source
  **/
  @Schema(required = true, description = "This field describes the source of the GeoLocation. . Enum options - GSLB_LOCATION_SRC_USER_CONFIGURED, GSLB_LOCATION_SRC_INHERIT_FROM_SITE, GSLB_LOCATION_SRC_FROM_GEODB. Field introduced in 17.1.1.")
  public String getSource() {
    return source;
  }

  public void setSource(String source) {
    this.source = source;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    GslbGeoLocation gslbGeoLocation = (GslbGeoLocation) o;
    return Objects.equals(this.location, gslbGeoLocation.location) &&
        Objects.equals(this.source, gslbGeoLocation.source);
  }

  @Override
  public int hashCode() {
    return Objects.hash(location, source);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class GslbGeoLocation {\n");
    
    sb.append("    location: ").append(toIndentedString(location)).append("\n");
    sb.append("    source: ").append(toIndentedString(source)).append("\n");
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