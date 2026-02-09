"""
Example: Using Identity for Agent Identity
"""
from payelink_agent_identity import Identity, ServiceEndpoint
from payelink_agent_identity.utils.constants import (
    VR_AUTHENTICATION,
    VR_ASSERTION,
    SERVICE_TYPE_MESSAGING
)

def create_agent_identity(agent_name: str, inbox_url: str):
    """
    Create an identity for an AI agent with messaging service
    """
    # Create service endpoint for agent inbox
    service = ServiceEndpoint(
        id="#agent-inbox",
        type=SERVICE_TYPE_MESSAGING,
        serviceEndpoint=inbox_url
    )
    
    # Create identity with authentication, assertion, and messaging service
    identity = Identity.create(
        verification_relationships=[VR_AUTHENTICATION, VR_ASSERTION],
        services=[service]
    )
    
    print(f"Created identity for agent: {agent_name}")
    print(f"DID: {identity.did}")
    print(f"\nAgent can use this identity to:")
    print("  - Authenticate itself (authentication)")
    print("  - Issue verifiable credentials (assertionMethod)")
    print(f"  - Receive messages at: {inbox_url}")
    
    return identity

if __name__ == "__main__":
    # Example: Create identity for a payment agent
    identity = create_agent_identity(
        agent_name="PaymentAgent",
        inbox_url="https://agent.payelink.com/inbox"
    )
    
    print("\n\nDID Document:")
    print(identity.document.json_ld(indent=2))
