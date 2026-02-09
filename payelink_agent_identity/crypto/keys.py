"""
Cryptographic key pair abstraction
"""
from pydantic import BaseModel


class KeyPair(BaseModel):
    """
    Cryptographic key pair
    """
    public_key: bytes
    private_key: bytes
    key_type: str
    
    class Config:
        arbitrary_types_allowed = True
