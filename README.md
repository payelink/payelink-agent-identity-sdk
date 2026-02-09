# PayeLink Agent Identity SDK

A production-ready, W3C DID Core v1.0 compliant Python SDK and CLI tool for creating, managing, and resolving Decentralized Identifiers (DIDs) for AI agents. Built with type safety, full specification compliance, and developer experience in mind, this SDK enables seamless integration of decentralized identity into agent-based systems.

The SDK provides a clean, intuitive API centered around the `Identity` abstraction, making it easy for developers to generate `did:key` identifiers, build compliant DID documents, and resolve existing DIDs—all while maintaining strict adherence to W3C standards. Whether you're building autonomous agents, multi-agent systems, or agent-to-agent communication protocols, this SDK provides the foundational identity layer your agents need.

Part of the PayeLink Agent SDK suite:
- `payelink-agent-identity-sdk` - This package (DID generation for agent identity)
- `payelink-agent-pay-sdk` - Agent-to-agent payments
- `payelink-agent-search-sdk` - Agent discovery and search

## Features

- ✅ **W3C DID Core v1.0 Compliant** - Full specification compliance
- ✅ **did:key Method** - Purely generative, no ledger required
- ✅ **Ed25519 Support** - Recommended cryptographic keys
- ✅ **DID Resolution** - Computational resolution for did:key
- ✅ **Type Safety** - Pydantic models for validation
- ✅ **CLI Tool** - Command-line interface for quick operations
- ✅ **SDK** - Programmatic access for agent integration

## Installation

```bash
pip install -e .
```

Or with development dependencies:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Using the SDK

```python
from payelink_agent_identity import Identity

# Create a new identity
identity = Identity.create()

print(identity.did)
print(identity.document.json(indent=2))

# Resolve an existing DID
identity = Identity.resolve("did:key:z6Mk...")
```

### Using the CLI

```bash
# Generate a new DID
payelink-agent-identity generate

# Generate with specific verification relationships
payelink-agent-identity generate -vr authentication -vr assertionMethod

# Generate with service endpoint
payelink-agent-identity generate --service-type MessagingService:https://agent.example.com/inbox

# Resolve a DID
payelink-agent-identity resolve did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK

# Validate DID syntax
payelink-agent-identity validate did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK
```

## SDK Usage

### Basic Identity Creation

```python
from payelink_agent_identity import Identity

# Create a new identity
identity = Identity.create()

# Access the DID and document
did = identity.did
document = identity.document
public_key = identity.public_key
private_key = identity.private_key  # ⚠️ Handle securely!

# Export document
print(identity.document.json(indent=2))
```

### Custom Verification Relationships

```python
from payelink_agent_identity import Identity
from payelink_agent_identity.utils.constants import (
    VR_AUTHENTICATION,
    VR_ASSERTION,
    VR_KEY_AGREEMENT
)

identity = Identity.create(
    verification_relationships=[
        VR_AUTHENTICATION,
        VR_ASSERTION,
        VR_KEY_AGREEMENT
    ]
)
```

### Adding Service Endpoints

```python
from payelink_agent_identity import Identity, ServiceEndpoint

service = ServiceEndpoint(
    id="#agent-inbox",
    type="MessagingService",
    serviceEndpoint="https://agent.example.com/inbox"
)

identity = Identity.create(services=[service])
```

### DID Resolution

```python
from payelink_agent_identity import Identity

# Resolve any did:key DID
identity = Identity.resolve("did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK")
print(identity.document.json(indent=2))
```

### Export Formats

```python
# Export as JSON
json_output = identity.document.json(indent=2)

# Export as JSON-LD
json_ld_output = identity.document.json_ld(indent=2)
```

## CLI Commands

### `generate`

Generate a new DID for an agent.

**Options:**
- `--key-type`: Cryptographic key type (default: Ed25519)
- `--verification-relationships` / `-vr`: Verification relationships (can specify multiple)
- `--service-type` / `-st`: Service endpoint (format: type:endpoint_url)
- `--output-format`: Output format (json or json-ld, default: json-ld)
- `--save-to`: Save DID document to file
- `--save-keys`: Save private key to .key file (⚠️ WARNING: Handle with care!)
- `--also-known-as` / `-aka`: Alternative identifiers (can specify multiple)

**Examples:**
```bash
# Basic generation
payelink-agent-identity generate

# With verification relationships
payelink-agent-identity generate -vr authentication -vr assertionMethod

# With service endpoint
payelink-agent-identity generate --service-type MessagingService:https://agent.example.com/inbox

# Save to file
payelink-agent-identity generate --save-to my-did.json --save-keys
```

### `resolve`

Resolve a DID to its document.

**Options:**
- `--output-format`: Output format (json or json-ld)

**Example:**
```bash
payelink-agent-identity resolve did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK
```

### `validate`

Validate DID syntax.

**Example:**
```bash
payelink-agent-identity validate did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK
```

### `verify-document`

Verify a DID document file is valid.

**Example:**
```bash
payelink-agent-identity verify-document my-did.json
```

## Architecture

The SDK is organized into the following modules:

- **`payelink_agent_identity.sdk`** - Core SDK classes (Identity, Generator, Resolver, DocumentBuilder)
- **`payelink_agent_identity.sdk.types`** - Pydantic models for DID documents
- **`payelink_agent_identity.crypto`** - Cryptographic key operations
- **`payelink_agent_identity.utils`** - Utilities (encoding, validation, constants)
- **`payelink_agent_identity.cli`** - CLI commands

## Security Considerations

⚠️ **IMPORTANT SECURITY NOTES:**

1. **Never expose private keys** in DID documents (W3C Spec Section 9.2)
2. **Store private keys securely** - Use proper key management systems
3. **Key rotation** - Support for key rotation is planned for future releases
4. **Verification method separation** - Use different keys for different purposes

## Examples

See the `examples/` directory for complete usage examples:

- `basic_generation.py` - Basic DID generation
- `agent_usage.py` - Creating DIDs for agents with services

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black payelink_did/
ruff check payelink_did/
```

## Specification Compliance

This implementation follows the [W3C DID Core v1.0](https://www.w3.org/TR/did-core/) specification:

- ✅ Section 3: Identifier syntax
- ✅ Section 4: Data model
- ✅ Section 5: Core properties
- ✅ Section 6: Representations (JSON, JSON-LD)
- ✅ Section 7: Resolution
- ✅ Section 8: Methods (did:key)

## License

MIT

## Contributing

Contributions welcome! Please see the project repository for guidelines.
