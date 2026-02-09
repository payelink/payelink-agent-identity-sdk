"""
PayeLink Agent Identity SDK - W3C DID Core v1.0 compliant SDK for agent identity
"""

# Primary API
from .sdk.identity import Identity

# Advanced API (for power users)
from .sdk.generator import DIDGenerator

# Type definitions
from .sdk.types import (
    DIDDocument,
    DIDGenerationResult,
    DIDResolutionResult,
    VerificationMethod,
    ServiceEndpoint,
)
from .crypto.keys import KeyPair

__version__ = "0.1.0"
__all__ = [
    # Primary API
    "Identity",
    # Advanced API
    "DIDGenerator",
    # Types
    "DIDDocument",
    "DIDGenerationResult",
    "DIDResolutionResult",
    "VerificationMethod",
    "ServiceEndpoint",
    "KeyPair",
]
