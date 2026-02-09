"""
Cryptographic key management for DIDs
Spec reference: Section 5.2 - Verification Methods
"""
from typing import Tuple
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey
)
from cryptography.hazmat.primitives import serialization

from ..crypto.keys import KeyPair


class KeyManager:
    """
    Manages cryptographic key generation and operations
    
    Security Note (from Spec Section 9):
    - Never expose private keys in DID documents
    - Store private keys securely
    - Support key rotation
    """
    
    @staticmethod
    def generate_ed25519_keypair() -> KeyPair:
        """
        Generate Ed25519 key pair (recommended for did:key)
        
        Spec: Section 5.2.1 - Verification Material
        Ed25519 is recommended for its security and performance
        
        Returns:
            KeyPair with 32-byte public and private keys
        """
        # Generate private key
        private_key = Ed25519PrivateKey.generate()
        
        # Get public key
        public_key = private_key.public_key()
        
        # Serialize to raw bytes
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        return KeyPair(
            public_key=public_bytes,
            private_key=private_bytes,
            key_type="Ed25519"
        )
    
    @staticmethod
    def public_key_from_bytes(public_bytes: bytes, key_type: str = "Ed25519") -> Ed25519PublicKey:
        """
        Reconstruct public key from bytes
        """
        if key_type == "Ed25519":
            return Ed25519PublicKey.from_public_bytes(public_bytes)
        else:
            raise ValueError(f"Unsupported key type: {key_type}")
    
    @staticmethod
    def validate_public_key(public_key: bytes, key_type: str = "Ed25519") -> bool:
        """
        Validate that public key is well-formed
        """
        if key_type == "Ed25519":
            # Ed25519 public keys are 32 bytes
            if len(public_key) != 32:
                return False
            try:
                Ed25519PublicKey.from_public_bytes(public_key)
                return True
            except Exception:
                return False
        return False
