"""
DID Document Builder
Spec reference: Section 5 - Core Properties
"""
from typing import List, Optional, Union
from .types import DIDDocument, VerificationMethod, ServiceEndpoint
from ..utils.encoding import MultibaseEncoder, MulticodecEncoder
from ..utils.constants import (
    DID_CONTEXT_V1,
    ED25519_2020_CONTEXT,
    VM_TYPE_ED25519_2020,
    VR_AUTHENTICATION,
    VR_ASSERTION,
    VR_KEY_AGREEMENT,
    VR_CAPABILITY_INVOCATION,
    VR_CAPABILITY_DELEGATION
)


class DIDDocumentBuilder:
    """
    Builds W3C compliant DID documents
    
    Spec compliance:
    - Section 5.1.1: id property (required)
    - Section 5.2: verificationMethod
    - Section 5.3: Verification relationships
    - Section 5.4: Services
    - Section 6.3: JSON-LD representation
    """
    
    def build(
        self,
        did: str,
        public_key: bytes,
        key_type: str = "Ed25519",
        verification_relationships: Optional[List[str]] = None,
        services: Optional[List[ServiceEndpoint]] = None,
        also_known_as: Optional[List[str]] = None,
        controller: Optional[Union[str, List[str]]] = None
    ) -> DIDDocument:
        """
        Build a complete DID document
        
        Args:
            did: The DID identifier (Spec 5.1.1)
            public_key: Raw public key bytes
            key_type: Type of key (default: Ed25519)
            verification_relationships: List of relationships to include
            services: Optional service endpoints (Spec 5.4)
            also_known_as: Alternative identifiers (Spec 5.1.3)
            controller: DID controller(s) (Spec 5.1.2)
        
        Returns:
            Complete DIDDocument
        """
        if verification_relationships is None:
            verification_relationships = [VR_AUTHENTICATION]
        
        # Build context (Spec 6.3.1)
        context = self._build_context(key_type)
        
        # Build verification method (Spec 5.2)
        verification_method = self._build_verification_method(
            did, public_key, key_type
        )
        
        # Build document
        doc_dict = {
            "@context": context,
            "id": did,
            "verificationMethod": [verification_method]
        }
        
        # Add verification relationships (Spec 5.3)
        vm_id = verification_method.id
        
        if VR_AUTHENTICATION in verification_relationships:
            doc_dict["authentication"] = [vm_id]
        
        if VR_ASSERTION in verification_relationships:
            doc_dict["assertionMethod"] = [vm_id]
        
        if VR_KEY_AGREEMENT in verification_relationships:
            doc_dict["keyAgreement"] = [vm_id]
        
        if VR_CAPABILITY_INVOCATION in verification_relationships:
            doc_dict["capabilityInvocation"] = [vm_id]
        
        if VR_CAPABILITY_DELEGATION in verification_relationships:
            doc_dict["capabilityDelegation"] = [vm_id]
        
        # Add optional properties
        if also_known_as:
            doc_dict["alsoKnownAs"] = also_known_as
        
        if controller:
            doc_dict["controller"] = controller
        
        if services:
            doc_dict["service"] = services
        
        return DIDDocument(**doc_dict)
    
    def _build_context(self, key_type: str) -> List[str]:
        """
        Build @context array based on key type
        
        Spec 6.3.1: JSON-LD context must include DID v1 context
        """
        contexts = [DID_CONTEXT_V1]
        
        if key_type == "Ed25519":
            contexts.append(ED25519_2020_CONTEXT)
        
        return contexts
    
    def _build_verification_method(
        self,
        did: str,
        public_key: bytes,
        key_type: str
    ) -> VerificationMethod:
        """
        Build verification method entry
        
        Spec 5.2: Each verification method must have id, type, controller,
        and verification material (publicKeyMultibase or publicKeyJwk)
        """
        # Create verification method ID (fragment identifier)
        # For did:key, use the same encoded key as fragment
        multicodec_key = MulticodecEncoder.encode_public_key(public_key, key_type)
        multibase_key = MultibaseEncoder.encode(multicodec_key)
        vm_id = f"{did}#{multibase_key}"
        
        # Encode public key as multibase (Spec 5.2.1)
        public_key_multibase = multibase_key
        
        # Determine verification method type
        vm_type = VM_TYPE_ED25519_2020 if key_type == "Ed25519" else "Unknown"
        
        # Only include publicKeyMultibase, not publicKeyJwk
        # publicKeyJwk will be None by default and excluded in export
        return VerificationMethod(
            id=vm_id,
            type=vm_type,
            controller=did,
            publicKeyMultibase=public_key_multibase
        )
    
    def add_service(
        self,
        document: DIDDocument,
        service_id: str,
        service_type: str,
        service_endpoint: Union[str, dict]
    ) -> DIDDocument:
        """
        Add a service to existing document
        
        Spec 5.4: Services enable communication with DID subject
        """
        service = ServiceEndpoint(
            id=service_id,
            type=service_type,
            serviceEndpoint=service_endpoint
        )
        
        if document.service is None:
            document.service = []
        
        document.service.append(service)
        
        return document
