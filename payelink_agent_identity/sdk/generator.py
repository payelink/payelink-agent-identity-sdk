"""
Main DID Generator
Spec reference: Section 1 - Introduction & Section 8.2 - Method Operations
"""
from typing import Optional, List, Dict, Any

from .key_manager import KeyManager
from .document_builder import DIDDocumentBuilder
from .resolver import DIDKeyResolver
from ..utils.encoding import create_did_key_identifier
from ..utils.constants import VR_AUTHENTICATION, VR_ASSERTION
from .types import DIDDocument, DIDGenerationResult, ServiceEndpoint


class DIDGenerator:
    """
    Main class for generating did:key DIDs
    
    Usage:
        generator = DIDGenerator()
        result = generator.generate()
        print(f"DID: {result.did}")
        print(f"Document: {result.document.model_dump_json(indent=2)}")
    """
    
    def __init__(self):
        self.key_manager = KeyManager()
        self.document_builder = DIDDocumentBuilder()
        self.resolver = DIDKeyResolver()
    
    def generate(
        self,
        key_type: str = "Ed25519",
        verification_relationships: Optional[List[str]] = None,
        services: Optional[List[ServiceEndpoint]] = None,
        also_known_as: Optional[List[str]] = None
    ) -> DIDGenerationResult:
        """
        Generate a new DID with document
        
        Args:
            key_type: Type of cryptographic key (default: Ed25519)
            verification_relationships: List of relationships to include
                Options: authentication, assertionMethod, keyAgreement,
                        capabilityInvocation, capabilityDelegation
            services: Optional service endpoints
            also_known_as: Optional alternative identifiers
            
        Returns:
            DIDGenerationResult containing DID, document, and keys
            
        Security Warning:
            The private key is returned but should be stored securely!
            Never expose private keys in DID documents (Spec 9.2)
        """
        # Default to authentication and assertion if not specified
        if verification_relationships is None:
            verification_relationships = [VR_AUTHENTICATION, VR_ASSERTION]
        
        # Step 1: Generate key pair
        key_pair = self.key_manager.generate_ed25519_keypair()
        
        # Step 2: Create DID identifier
        did = create_did_key_identifier(key_pair.public_key, key_type)
        
        # Step 3: Build DID document
        document = self.document_builder.build(
            did=did,
            public_key=key_pair.public_key,
            key_type=key_type,
            verification_relationships=verification_relationships,
            services=services,
            also_known_as=also_known_as
        )
        
        # Step 4: Return result
        return DIDGenerationResult(
            did=did,
            document=document,
            public_key=key_pair.public_key,
            private_key=key_pair.private_key,
            key_type=key_type
        )
    
    def generate_from_existing_key(
        self,
        public_key: bytes,
        key_type: str = "Ed25519",
        verification_relationships: Optional[List[str]] = None,
        services: Optional[List[ServiceEndpoint]] = None
    ) -> Dict[str, Any]:
        """
        Generate DID document from existing public key
        
        Useful when you already have keys and just need the DID/document
        """
        did = create_did_key_identifier(public_key, key_type)
        
        if verification_relationships is None:
            verification_relationships = [VR_AUTHENTICATION, VR_ASSERTION]
        
        document = self.document_builder.build(
            did=did,
            public_key=public_key,
            key_type=key_type,
            verification_relationships=verification_relationships,
            services=services
        )
        
        return {
            "did": did,
            "document": document
        }
    
    def resolve(self, did: str) -> DIDDocument:
        """
        Resolve a did:key DID to its document
        
        For did:key, the document can be generated from the DID itself
        
        Spec: Section 7.1 - DID Resolution
        """
        return self.resolver.resolve(did)
    
    def export_json(self, document: DIDDocument, indent: int = 2) -> str:
        """
        Export DID document as JSON
        
        Spec: Section 6.2 - JSON Representation
        """
        # Exclude None values and empty lists/collections
        doc_dict = document.model_dump(
            by_alias=True,
            exclude_none=True,
            exclude_unset=False
        )
        
        # Remove empty lists and empty dicts
        cleaned_dict = self._remove_empty_fields(doc_dict)
        
        import json
        return json.dumps(cleaned_dict, indent=indent)
    
    def export_json_ld(self, document: DIDDocument, indent: int = 2) -> str:
        """
        Export DID document as JSON-LD
        
        Spec: Section 6.3 - JSON-LD Representation
        
        For did:key with Ed25519, we include the Ed25519 context
        """
        # Exclude None values and empty lists/collections
        doc_dict = document.model_dump(
            by_alias=True,
            exclude_none=True,
            exclude_unset=False
        )
        
        # Remove empty lists and empty dicts
        cleaned_dict = self._remove_empty_fields(doc_dict)
        
        import json
        return json.dumps(cleaned_dict, indent=indent)
    
    @staticmethod
    def _remove_empty_fields(data):
        """
        Recursively remove None values, empty lists, and empty dicts
        to produce cleaner output without noise
        """
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                cleaned_value = DIDGenerator._remove_empty_fields(value)
                # Skip None, empty lists, and empty dicts
                if cleaned_value is None:
                    continue
                if isinstance(cleaned_value, list) and len(cleaned_value) == 0:
                    continue
                if isinstance(cleaned_value, dict) and len(cleaned_value) == 0:
                    continue
                result[key] = cleaned_value
            return result
        elif isinstance(data, list):
            # Clean list items and filter out None values
            cleaned = [DIDGenerator._remove_empty_fields(item) for item in data]
            return [item for item in cleaned if item is not None]
        else:
            return data
