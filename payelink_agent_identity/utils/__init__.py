"""Utility modules for DID operations"""

from .constants import *
from .encoding import (
    MultibaseEncoder,
    MulticodecEncoder,
    create_did_key_identifier,
    extract_public_key_from_did,
)
from .validation import (
    validate_did_syntax,
    parse_did,
    validate_did_url,
    validate_verification_method_id,
)

__all__ = [
    "MultibaseEncoder",
    "MulticodecEncoder",
    "create_did_key_identifier",
    "extract_public_key_from_did",
    "validate_did_syntax",
    "parse_did",
    "validate_did_url",
    "validate_verification_method_id",
]
