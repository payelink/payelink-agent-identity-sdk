"""
Identity class - Primary API for agent identity management
"""
from typing import Optional, List
from .generator import DIDGenerator
from .types import DIDDocument, ServiceEndpoint


class Identity:
    """
    Represents an agent identity with a DID and associated document.
    
    This is the primary API for working with agent identities.
    Supports multiple DID methods (did:key, did:payelink, etc.)
    
    Usage:
        # Create a new identity
        identity = Identity.create()
        print(identity.did)
        print(identity.document.json(indent=2))
        
        # Resolve an existing DID
        identity = Identity.resolve("did:key:z6Mk...")
    """
    
    def __init__(
        self,
        did: str,
        document: DIDDocument,
        public_key: bytes,
        private_key: Optional[bytes] = None,
        key_type: str = "Ed25519"
    ):
        """
        Initialize an Identity instance.
        
        Args:
            did: The DID identifier
            document: The DID document
            public_key: Public key bytes
            private_key: Private key bytes (optional, for new identities)
            key_type: Type of cryptographic key
        """
        self._did = did
        self._document = document
        self._public_key = public_key
        self._private_key = private_key
        self._key_type = key_type
        self._generator = DIDGenerator()
    
    @property
    def did(self) -> str:
        """The DID identifier"""
        return self._did
    
    @property
    def document(self) -> DIDDocument:
        """The DID document"""
        return self._document
    
    @property
    def public_key(self) -> bytes:
        """Public key bytes"""
        return self._public_key
    
    @property
    def private_key(self) -> Optional[bytes]:
        """Private key bytes (None if not available)"""
        return self._private_key
    
    @property
    def key_type(self) -> str:
        """Cryptographic key type"""
        return self._key_type
    
    @classmethod
    def create(
        cls,
        key_type: str = "Ed25519",
        verification_relationships: Optional[List[str]] = None,
        services: Optional[List[ServiceEndpoint]] = None,
        also_known_as: Optional[List[str]] = None,
        method: str = "key"
    ) -> "Identity":
        """
        Create a new identity with a DID.
        
        Args:
            key_type: Type of cryptographic key (default: Ed25519)
            verification_relationships: List of verification relationships
                Options: authentication, assertionMethod, keyAgreement,
                        capabilityInvocation, capabilityDelegation
            services: Optional service endpoints
            also_known_as: Optional alternative identifiers
            method: DID method to use (default: "key" for did:key)
            
        Returns:
            Identity instance with new DID and document
            
        Example:
            identity = Identity.create()
            print(identity.did)
        """
        generator = DIDGenerator()
        
        # For now, only support did:key method
        if method != "key":
            raise ValueError(f"Unsupported DID method: {method}. Only 'key' is currently supported.")
        
        result = generator.generate(
            key_type=key_type,
            verification_relationships=verification_relationships,
            services=services,
            also_known_as=also_known_as
        )
        
        return cls(
            did=result.did,
            document=result.document,
            public_key=result.public_key,
            private_key=result.private_key,
            key_type=result.key_type
        )
    
    @classmethod
    def resolve(cls, did: str) -> "Identity":
        """
        Resolve an existing DID to get its identity.
        
        Args:
            did: The DID to resolve (e.g., "did:key:z6Mk...")
            
        Returns:
            Identity instance with resolved DID and document
            
        Example:
            identity = Identity.resolve("did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK")
        """
        generator = DIDGenerator()
        document = generator.resolve(did)
        
        # Extract public key from DID for did:key method
        if did.startswith("did:key:"):
            from ..utils.encoding import extract_public_key_from_did
            key_type, public_key = extract_public_key_from_did(did)
        else:
            raise ValueError(f"Cannot extract key from DID method: {did.split(':')[1]}")
        
        return cls(
            did=did,
            document=document,
            public_key=public_key,
            private_key=None,  # Cannot extract private key from DID
            key_type=key_type
        )
    
    @classmethod
    def from_key(
        cls,
        public_key: bytes,
        key_type: str = "Ed25519",
        verification_relationships: Optional[List[str]] = None,
        services: Optional[List[ServiceEndpoint]] = None
    ) -> "Identity":
        """
        Create an identity from an existing public key.
        
        Useful when you already have keys and just need the DID/document.
        
        Args:
            public_key: Existing public key bytes
            key_type: Type of key (default: Ed25519)
            verification_relationships: List of verification relationships
            services: Optional service endpoints
            
        Returns:
            Identity instance (without private key)
        """
        generator = DIDGenerator()
        result = generator.generate_from_existing_key(
            public_key=public_key,
            key_type=key_type,
            verification_relationships=verification_relationships,
            services=services
        )
        
        return cls(
            did=result["did"],
            document=result["document"],
            public_key=public_key,
            private_key=None,  # Not available when using existing key
            key_type=key_type
        )
    
    def __repr__(self) -> str:
        """String representation of the identity"""
        return f"Identity(did={self._did}, key_type={self._key_type})"


# Add json() method to DIDDocument for convenience
def _document_json(self, indent: int = 2) -> str:
    """Export DID document as JSON"""
    generator = DIDGenerator()
    return generator.export_json(self, indent=indent)


def _document_json_ld(self, indent: int = 2) -> str:
    """Export DID document as JSON-LD"""
    generator = DIDGenerator()
    return generator.export_json_ld(self, indent=indent)


# Monkey-patch DIDDocument to add json() method
DIDDocument.json = _document_json
DIDDocument.json_ld = _document_json_ld
