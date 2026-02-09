"""
DID Resolution for did:key method
Spec reference: Section 7.1 - DID Resolution
"""
from typing import Dict, Any

from ..utils.encoding import extract_public_key_from_did
from ..utils.validation import validate_did_syntax
from .document_builder import DIDDocumentBuilder
from .types import DIDDocument, DIDResolutionResult
from ..utils.constants import VR_AUTHENTICATION, VR_ASSERTION


class DIDKeyResolver:
    """
    Resolver for did:key method
    
    For did:key, resolution is purely computational:
    1. Parse the DID to extract public key
    2. Generate DID document from public key
    
    Spec: Section 7.1 - DID Resolution
    """
    
    def __init__(self):
        self.document_builder = DIDDocumentBuilder()
    
    def resolve(self, did: str) -> DIDDocument:
        """
        Resolve did:key to DID document
        
        Args:
            did: The DID to resolve (e.g., did:key:z6Mk...)
            
        Returns:
            DIDDocument
            
        Raises:
            ValueError: If DID is invalid or unsupported
        """
        # Validate DID syntax (Spec 3.1)
        if not validate_did_syntax(did):
            raise ValueError(f"Invalid DID syntax: {did}")
        
        # Only support did:key for now
        if not did.startswith("did:key:"):
            raise ValueError(f"Unsupported DID method. Only did:key is supported.")
        
        # Extract public key from DID
        try:
            key_type, public_key = extract_public_key_from_did(did)
        except Exception as e:
            raise ValueError(f"Failed to extract public key from DID: {e}")
        
        # Build DID document
        document = self.document_builder.build(
            did=did,
            public_key=public_key,
            key_type=key_type,
            verification_relationships=[VR_AUTHENTICATION, VR_ASSERTION]
        )
        
        return document
    
    def resolve_with_metadata(self, did: str) -> DIDResolutionResult:
        """
        Resolve with full metadata structure
        
        Spec: Section 7.1 - Returns didResolutionMetadata, didDocument, didDocumentMetadata
        """
        try:
            document = self.resolve(did)
            
            return DIDResolutionResult(
                didResolutionMetadata={
                    "contentType": "application/did+ld+json"
                },
                didDocument=document,
                didDocumentMetadata={}
            )
        except Exception as e:
            # Return error in metadata (Spec 7.1.2)
            return DIDResolutionResult(
                didResolutionMetadata={
                    "error": "notFound" if "extract" in str(e) else "invalidDid",
                    "errorMessage": str(e)
                },
                didDocument=None,
                didDocumentMetadata={}
            )
