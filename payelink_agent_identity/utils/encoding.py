"""
Multibase and multicodec encoding for DID identifiers
Spec reference: Section 3.1 - DID Syntax

did:key format: did:key:<multibase-encoded-multicodec-public-key>
"""
import base58
from typing import Tuple

from .constants import MULTICODEC_ED25519_PUB, MULTIBASE_BASE58BTC


class MultibaseEncoder:
    """
    Multibase encoding/decoding
    Reference: https://github.com/multiformats/multibase
    """
    
    @staticmethod
    def encode(data: bytes, encoding: str = 'base58btc') -> str:
        """
        Encode bytes with multibase prefix
        
        For did:key, we use base58btc (prefix 'z')
        
        Args:
            data: Raw bytes to encode
            encoding: Encoding type (default: base58btc)
            
        Returns:
            Multibase-encoded string with prefix
        """
        if encoding == 'base58btc':
            encoded = base58.b58encode(data).decode('ascii')
            return f"{MULTIBASE_BASE58BTC}{encoded}"
        else:
            raise ValueError(f"Unsupported encoding: {encoding}")
    
    @staticmethod
    def decode(multibase_string: str) -> Tuple[str, bytes]:
        """
        Decode multibase string
        
        Returns:
            Tuple of (encoding_type, decoded_bytes)
        """
        if not multibase_string:
            raise ValueError("Empty multibase string")
        
        prefix = multibase_string[0]
        encoded = multibase_string[1:]
        
        if prefix == MULTIBASE_BASE58BTC:
            decoded = base58.b58decode(encoded)
            return ('base58btc', decoded)
        else:
            raise ValueError(f"Unsupported multibase prefix: {prefix}")


class MulticodecEncoder:
    """
    Multicodec encoding for key types
    Reference: https://github.com/multiformats/multicodec
    """
    
    @staticmethod
    def encode_public_key(public_key: bytes, key_type: str = "Ed25519") -> bytes:
        """
        Encode public key with multicodec prefix
        
        For Ed25519: prefix is 0xed (1 byte)
        
        Args:
            public_key: Raw public key bytes
            key_type: Type of key (default: Ed25519)
            
        Returns:
            Multicodec-prefixed bytes
        """
        if key_type == "Ed25519":
            # Ed25519 public key multicodec is 0xed
            prefix = bytes([MULTICODEC_ED25519_PUB])
            return prefix + public_key
        else:
            raise ValueError(f"Unsupported key type: {key_type}")
    
    @staticmethod
    def decode_public_key(encoded: bytes) -> Tuple[str, bytes]:
        """
        Decode multicodec-prefixed public key
        
        Returns:
            Tuple of (key_type, raw_public_key)
        """
        if not encoded:
            raise ValueError("Empty encoded data")
        
        prefix = encoded[0]
        key_data = encoded[1:]
        
        if prefix == MULTICODEC_ED25519_PUB:
            return ("Ed25519", key_data)
        else:
            raise ValueError(f"Unknown multicodec prefix: 0x{prefix:02x}")


def create_did_key_identifier(public_key: bytes, key_type: str = "Ed25519") -> str:
    """
    Create did:key identifier from public key
    
    Process:
    1. Add multicodec prefix to public key
    2. Encode with multibase (base58btc)
    3. Construct DID: did:key:<encoded-key>
    
    Spec: https://w3c-ccg.github.io/did-method-key/
    
    Args:
        public_key: Raw public key bytes (32 bytes for Ed25519)
        key_type: Type of key
        
    Returns:
        Complete DID string (e.g., did:key:z6Mk...)
    """
    # Step 1: Add multicodec prefix
    multicodec_key = MulticodecEncoder.encode_public_key(public_key, key_type)
    
    # Step 2: Encode with multibase
    multibase_key = MultibaseEncoder.encode(multicodec_key)
    
    # Step 3: Construct DID
    did = f"did:key:{multibase_key}"
    
    return did


def extract_public_key_from_did(did: str) -> Tuple[str, bytes]:
    """
    Extract public key from did:key identifier
    
    This enables resolution of did:key DIDs
    
    Args:
        did: DID string (e.g., did:key:z6Mk...)
        
    Returns:
        Tuple of (key_type, public_key_bytes)
    """
    if not did.startswith("did:key:"):
        raise ValueError(f"Invalid did:key identifier: {did}")
    
    # Extract multibase-encoded portion
    multibase_key = did[8:]  # Remove "did:key:" prefix
    
    # Decode multibase
    encoding, multicodec_key = MultibaseEncoder.decode(multibase_key)
    
    # Decode multicodec
    key_type, public_key = MulticodecEncoder.decode_public_key(multicodec_key)
    
    return (key_type, public_key)
