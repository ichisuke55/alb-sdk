package models

// This file is auto-generated.
// Please contact avi-sdk@avinetworks.com for any change requests.

// SSOPolicy s s o policy
// swagger:model SSOPolicy
type SSOPolicy struct {

	// UNIX time since epoch in microseconds. Units(MICROSECONDS).
	// Read Only: true
	LastModified *string `json:"_last_modified,omitempty"`

	// Authentication Policy Settings. Field introduced in 18.2.1.
	// Required: true
	AuthenticationPolicy *AuthenticationPolicy `json:"authentication_policy"`

	// Name of the SSO Policy. Field introduced in 18.2.3.
	// Required: true
	Name *string `json:"name"`

	// UUID of the Tenant. It is a reference to an object of type Tenant. Field introduced in 18.2.3.
	TenantRef *string `json:"tenant_ref,omitempty"`

	// url
	// Read Only: true
	URL *string `json:"url,omitempty"`

	// UUID of the SSO Policy. Field introduced in 18.2.3.
	UUID *string `json:"uuid,omitempty"`
}
