"""
Constants from W3C DID Core specification
"""

# Spec Section 6.3.1: JSON-LD Contexts
DID_CONTEXT_V1 = "https://www.w3.org/ns/did/v1"
ED25519_2020_CONTEXT = "https://w3id.org/security/suites/ed25519-2020/v1"
JWS_2020_CONTEXT = "https://w3id.org/security/suites/jws-2020/v1"

# Multicodec prefixes (for did:key)
# Reference: https://github.com/multiformats/multicodec
MULTICODEC_ED25519_PUB = 0xED  # Ed25519 public key
MULTICODEC_ED25519_PRIV = 0x1300  # Ed25519 private key (for reference, never expose)
MULTICODEC_X25519_PUB = 0xEC  # X25519 public key (key agreement)

# Multibase prefixes
# Reference: https://github.com/multiformats/multibase
MULTIBASE_BASE58BTC = 'z'  # base58btc encoding

# Verification method types (registered in DID Spec Registries)
VM_TYPE_ED25519_2020 = "Ed25519VerificationKey2020"
VM_TYPE_ED25519_2018 = "Ed25519VerificationKey2018"  # Legacy
VM_TYPE_X25519_2019 = "X25519KeyAgreementKey2019"
VM_TYPE_JWK_2020 = "JsonWebKey2020"

# Verification relationships (Spec Section 5.3)
VR_AUTHENTICATION = "authentication"
VR_ASSERTION = "assertionMethod"
VR_KEY_AGREEMENT = "keyAgreement"
VR_CAPABILITY_INVOCATION = "capabilityInvocation"
VR_CAPABILITY_DELEGATION = "capabilityDelegation"

# Common service types (examples, not exhaustive)
SERVICE_TYPE_MESSAGING = "MessagingService"
SERVICE_TYPE_LINKED_DOMAINS = "LinkedDomains"
SERVICE_TYPE_DID_COMM = "DIDCommMessaging"
