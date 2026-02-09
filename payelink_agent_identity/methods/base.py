"""
Base class for DID method implementations
Future extensibility for adding did:web, did:peer, etc.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class DIDMethod(ABC):
    """
    Base interface for DID method implementations
    """
    
    @abstractmethod
    def generate(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a new DID using this method"""
        pass
    
    @abstractmethod
    def resolve(self, did: str) -> Dict[str, Any]:
        """Resolve a DID to its document"""
        pass
