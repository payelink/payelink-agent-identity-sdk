"""
DID validation utilities
Spec reference: Section 3 - Identifier
"""
import re
from typing import Tuple


def validate_did_syntax(did: str) -> bool:
    """
    Validate DID conforms to generic DID syntax
    
    Spec 3.1: DID Syntax ABNF
    did = "did:" method-name ":" method-specific-id
    """
    # Basic regex for DID syntax
    # More permissive than full ABNF but catches major issues
    did_pattern = r'^did:[a-z0-9]+:[a-zA-Z0-9._\-:]+$'
    
    return bool(re.match(did_pattern, did))


def parse_did(did: str) -> Tuple[str, str]:
    """
    Parse DID into method and method-specific-id
    
    Returns:
        Tuple of (method_name, method_specific_id)
    """
    if not did.startswith('did:'):
        raise ValueError(f"Invalid DID: {did}")
    
    parts = did.split(':', 2)
    
    if len(parts) < 3:
        raise ValueError(f"Invalid DID structure: {did}")
    
    return (parts[1], parts[2])


def validate_did_url(did_url: str) -> bool:
    """
    Validate DID URL syntax
    
    Spec 3.2: DID URL may include path, query, fragment
    did-url = did path-abempty [ "?" query ] [ "#" fragment ]
    """
    # Split on first occurrence of ?, #, or /
    base_did = did_url.split('?')[0].split('#')[0].split('/')[0]
    
    return validate_did_syntax(base_did)


def validate_verification_method_id(vm_id: str) -> bool:
    """
    Validate verification method ID is a valid DID URL
    
    Spec 5.2: id must be a DID URL
    """
    # Can be relative (#key-1) or absolute (did:example:123#key-1)
    if vm_id.startswith('#'):
        return True
    
    return validate_did_url(vm_id)
