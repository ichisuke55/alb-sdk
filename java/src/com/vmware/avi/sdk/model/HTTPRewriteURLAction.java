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
import com.vmware.avi.sdk.model.URIParam;
import com.vmware.avi.sdk.model.URIParamQuery;
import io.swagger.v3.oas.annotations.media.Schema;
/**
 * HTTPRewriteURLAction
 */

@javax.annotation.Generated(value = "io.swagger.codegen.v3.generators.java.JavaClientCodegen", date = "2020-03-12T12:27:26.755+05:30[Asia/Kolkata]")
public class HTTPRewriteURLAction {
  @JsonProperty("host_hdr")
  private URIParam hostHdr = null;

  @JsonProperty("path")
  private URIParam path = null;

  @JsonProperty("query")
  private URIParamQuery query = null;

  public HTTPRewriteURLAction hostHdr(URIParam hostHdr) {
    this.hostHdr = hostHdr;
    return this;
  }

   /**
   * Get hostHdr
   * @return hostHdr
  **/
  @Schema(description = "")
  public URIParam getHostHdr() {
    return hostHdr;
  }

  public void setHostHdr(URIParam hostHdr) {
    this.hostHdr = hostHdr;
  }

  public HTTPRewriteURLAction path(URIParam path) {
    this.path = path;
    return this;
  }

   /**
   * Get path
   * @return path
  **/
  @Schema(description = "")
  public URIParam getPath() {
    return path;
  }

  public void setPath(URIParam path) {
    this.path = path;
  }

  public HTTPRewriteURLAction query(URIParamQuery query) {
    this.query = query;
    return this;
  }

   /**
   * Get query
   * @return query
  **/
  @Schema(description = "")
  public URIParamQuery getQuery() {
    return query;
  }

  public void setQuery(URIParamQuery query) {
    this.query = query;
  }


  @Override
  public boolean equals(java.lang.Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    HTTPRewriteURLAction htTPRewriteURLAction = (HTTPRewriteURLAction) o;
    return Objects.equals(this.hostHdr, htTPRewriteURLAction.hostHdr) &&
        Objects.equals(this.path, htTPRewriteURLAction.path) &&
        Objects.equals(this.query, htTPRewriteURLAction.query);
  }

  @Override
  public int hashCode() {
    return Objects.hash(hostHdr, path, query);
  }


  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    sb.append("class HTTPRewriteURLAction {\n");
    
    sb.append("    hostHdr: ").append(toIndentedString(hostHdr)).append("\n");
    sb.append("    path: ").append(toIndentedString(path)).append("\n");
    sb.append("    query: ").append(toIndentedString(query)).append("\n");
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