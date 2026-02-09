"""
DID document data types following W3C DID Core v1.0
Spec reference: https://www.w3.org/TR/did-core/#data-model
"""
from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field, field_validator


class VerificationMethod(BaseModel):
    """
    Spec: Section 5.2 - Verification Methods
    """
    id: str = Field(..., description="DID URL for this verification method")
    type: str = Field(..., description="Verification method type")
    controller: str = Field(..., description="DID of the controller")
    publicKeyMultibase: Optional[str] = Field(default=None, description="Multibase-encoded public key")
    publicKeyJwk: Optional[Dict[str, Any]] = Field(default=None, description="JSON Web Key")
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Ensure id is a valid DID URL (Spec 3.2)"""
        if not (v.startswith('did:') or v.startswith('#')):
            raise ValueError(f"Invalid verification method id: {v}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK#z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK",
                "type": "Ed25519VerificationKey2020",
                "controller": "did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK",
                "publicKeyMultibase": "z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK"
            }
        }


class ServiceEndpoint(BaseModel):
    """
    Spec: Section 5.4 - Services
    """
    id: str = Field(..., description="Service ID (must be URI)")
    type: str = Field(..., description="Service type")
    serviceEndpoint: Union[str, Dict[str, Any], List[Union[str, Dict[str, Any]]]] = Field(
        ..., 
        description="Service endpoint URL or object"
    )
    
    @field_validator('serviceEndpoint')
    @classmethod
    def validate_endpoint(cls, v):
        """Ensure serviceEndpoint is valid URI or structure (Spec 5.4)"""
        if isinstance(v, str):
            if not (v.startswith('http://') or v.startswith('https://') or v.startswith('did:')):
                raise ValueError(f"Invalid service endpoint URL: {v}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "did:key:z6Mk...#agent-inbox",
                "type": "MessagingService",
                "serviceEndpoint": "https://agent.example.com/inbox"
            }
        }


class DIDDocument(BaseModel):
    """
    Complete DID Document structure
    Spec: Section 5 - Core Properties
    """
    context: Union[str, List[Union[str, Dict[str, Any]]]] = Field(
        alias="@context",
        default=["https://www.w3.org/ns/did/v1"]
    )
    id: str = Field(..., description="The DID subject (Spec 5.1.1)")
    alsoKnownAs: Optional[List[str]] = Field(None, description="Alternative identifiers (Spec 5.1.3)")
    controller: Optional[Union[str, List[str]]] = Field(None, description="DID controller(s) (Spec 5.1.2)")
    verificationMethod: Optional[List[VerificationMethod]] = Field(None, description="Verification methods (Spec 5.2)")
    authentication: Optional[List[Union[str, VerificationMethod]]] = Field(None, description="Authentication (Spec 5.3.1)")
    assertionMethod: Optional[List[Union[str, VerificationMethod]]] = Field(None, description="Assertion (Spec 5.3.2)")
    keyAgreement: Optional[List[Union[str, VerificationMethod]]] = Field(None, description="Key agreement (Spec 5.3.3)")
    capabilityInvocation: Optional[List[Union[str, VerificationMethod]]] = Field(None, description="Capability invocation (Spec 5.3.4)")
    capabilityDelegation: Optional[List[Union[str, VerificationMethod]]] = Field(None, description="Capability delegation (Spec 5.3.5)")
    service: Optional[List[ServiceEndpoint]] = Field(None, description="Services (Spec 5.4)")
    
    @field_validator('id')
    @classmethod
    def validate_did(cls, v: str) -> str:
        """Ensure id conforms to DID syntax (Spec 3.1)"""
        if not v.startswith('did:'):
            raise ValueError(f"Invalid DID: {v}")
        return v
    
    class Config:
        populate_by_name = True  # Allow using '@context' as field name
        json_encoders = {
            # Ensure None values are excluded
        }
        json_schema_extra = {
            "example": {
                "@context": [
                    "https://www.w3.org/ns/did/v1",
                    "https://w3id.org/security/suites/ed25519-2020/v1"
                ],
                "id": "did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK",
                "verificationMethod": [{
                    "id": "did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK#z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK",
                    "type": "Ed25519VerificationKey2020",
                    "controller": "did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK",
                    "publicKeyMultibase": "z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK"
                }],
                "authentication": [
                    "did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK#z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK"
                ]
            }
        }


class DIDResolutionResult(BaseModel):
    """
    DID Resolution result
    Spec: Section 7.1 - DID Resolution
    """
    didResolutionMetadata: Dict[str, Any] = Field(default_factory=dict)
    didDocument: Optional[DIDDocument] = None
    didDocumentMetadata: Dict[str, Any] = Field(default_factory=dict)


class DIDGenerationResult(BaseModel):
    """
    Result of DID generation (not in spec, but practical)
    """
    did: str
    document: DIDDocument
    public_key: bytes
    private_key: bytes  # WARNING: Handle with extreme care!
    key_type: str
    
    class Config:
        arbitrary_types_allowed = True
