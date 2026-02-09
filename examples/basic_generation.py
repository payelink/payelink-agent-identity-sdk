"""
Basic Identity Creation Example
"""
from payelink_agent_identity import Identity

def main():
    # Create a new identity
    print("Creating a new identity...")
    identity = Identity.create()
    
    print(f"\n✓ Created Identity")
    print(f"✓ DID: {identity.did}")
    print(f"✓ Key Type: {identity.key_type}")
    print(f"✓ Public Key (hex): {identity.public_key.hex()}")
    
    # Export document as JSON-LD
    print("\nDID Document (JSON-LD):")
    print(identity.document.json_ld(indent=2))
    
    # Resolve the DID to verify it works
    print("\n\nResolving DID to verify...")
    resolved_identity = Identity.resolve(identity.did)
    print(f"✓ Successfully resolved DID: {resolved_identity.did}")
    
    print("\n⚠️  WARNING: Private key not shown for security!")
    print("   Store the private key securely if you need to use this identity for signing.")

if __name__ == "__main__":
    main()
