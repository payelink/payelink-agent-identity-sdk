"""
CLI commands for DID generation and management
"""
import click
import json
import sys
from pathlib import Path
from typing import Optional

from ..sdk.generator import DIDGenerator
from ..sdk.types import ServiceEndpoint
from ..utils.constants import (
    VR_AUTHENTICATION,
    VR_ASSERTION,
    VR_KEY_AGREEMENT,
    VR_CAPABILITY_INVOCATION,
    VR_CAPABILITY_DELEGATION,
    SERVICE_TYPE_MESSAGING,
    SERVICE_TYPE_DID_COMM
)


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """
    PayeLink Agent Identity SDK - Generate and manage Decentralized Identifiers
    
    A W3C DID Core v1.0 compliant tool for generating did:key DIDs for agent identity.
    Part of the PayeLink Agent SDK suite.
    """
    pass


@cli.command()
@click.option(
    '--key-type',
    type=click.Choice(['Ed25519'], case_sensitive=False),
    default='Ed25519',
    help='Cryptographic key type (default: Ed25519)'
)
@click.option(
    '--verification-relationships',
    '-vr',
    multiple=True,
    type=click.Choice([
        VR_AUTHENTICATION,
        VR_ASSERTION,
        VR_KEY_AGREEMENT,
        VR_CAPABILITY_INVOCATION,
        VR_CAPABILITY_DELEGATION
    ]),
    help='Verification relationships to include (can specify multiple times)'
)
@click.option(
    '--service-type',
    '-st',
    help='Add a service endpoint (format: type:endpoint_url)'
)
@click.option(
    '--output-format',
    type=click.Choice(['json', 'json-ld']),
    default='json-ld',
    help='Output format (default: json-ld)'
)
@click.option(
    '--save-to',
    type=click.Path(),
    help='Save DID document to file'
)
@click.option(
    '--save-keys/--no-save-keys',
    default=False,
    help='Save private key to .key file (WARNING: Handle with care!)'
)
@click.option(
    '--also-known-as',
    '-aka',
    multiple=True,
    help='Alternative identifiers (can specify multiple times)'
)
def generate(
    key_type,
    verification_relationships,
    service_type,
    output_format,
    save_to,
    save_keys,
    also_known_as
):
    """
    Generate a new DID for an agent
    
    Example:
        payelink-agent-identity generate
        payelink-agent-identity generate -vr authentication -vr assertionMethod
        payelink-agent-identity generate --service-type MessagingService:https://agent.example.com/inbox
    """
    try:
        generator = DIDGenerator()
        
        # Parse verification relationships
        vr_list = list(verification_relationships) if verification_relationships else None
        
        # Parse service endpoint
        services = None
        if service_type:
            parts = service_type.split(':', 1)
            if len(parts) == 2:
                services = [ServiceEndpoint(
                    id=f"#service-1",
                    type=parts[0],
                    serviceEndpoint=parts[1]
                )]
        
        # Parse also known as
        aka_list = list(also_known_as) if also_known_as else None
        
        # Generate DID
        result = generator.generate(
            key_type=key_type,
            verification_relationships=vr_list,
            services=services,
            also_known_as=aka_list
        )
        
        # Display results
        click.echo(click.style("\n✓ DID Generated Successfully!", fg='green', bold=True))
        click.echo(f"\nDID: {click.style(result.did, fg='cyan', bold=True)}")
        
        # Export document
        if output_format == 'json-ld':
            doc_output = generator.export_json_ld(result.document)
        else:
            doc_output = generator.export_json(result.document)
        
        click.echo(f"\nDID Document ({output_format}):")
        click.echo(doc_output)
        
        # Save to file if requested
        if save_to:
            output_path = Path(save_to)
            output_path.write_text(doc_output)
            click.echo(f"\n✓ DID document saved to: {output_path}")
            
            if save_keys:
                key_path = output_path.with_suffix('.key')
                key_data = {
                    "did": result.did,
                    "private_key": result.private_key.hex(),
                    "public_key": result.public_key.hex(),
                    "key_type": result.key_type,
                    "WARNING": "Keep this file secure! Never share private keys!"
                }
                key_path.write_text(json.dumps(key_data, indent=2))
                click.echo(click.style(
                    f"⚠  Private key saved to: {key_path} (KEEP SECURE!)",
                    fg='yellow',
                    bold=True
                ))
        
        # Security warning if keys not saved
        if not save_keys:
            click.echo(click.style(
                "\n⚠  Private key not saved. You won't be able to use this DID for signing!",
                fg='yellow'
            ))
        
    except Exception as e:
        click.echo(click.style(f"\n✗ Error: {str(e)}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('did')
@click.option(
    '--output-format',
    type=click.Choice(['json', 'json-ld']),
    default='json-ld',
    help='Output format'
)
def resolve(did, output_format):
    """
    Resolve a DID to its document
    
    Example:
        payelink-agent-identity resolve did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK
    """
    try:
        generator = DIDGenerator()
        document = generator.resolve(did)
        
        if output_format == 'json-ld':
            output = generator.export_json_ld(document)
        else:
            output = generator.export_json(document)
        
        click.echo(output)
        
    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('did')
def validate(did):
    """
    Validate DID syntax
    
    Example:
        payelink-agent-identity validate did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK
    """
    from ..utils.validation import validate_did_syntax, parse_did
    
    if validate_did_syntax(did):
        method, method_id = parse_did(did)
        click.echo(click.style("✓ Valid DID syntax", fg='green'))
        click.echo(f"Method: {method}")
        click.echo(f"Method-specific ID: {method_id}")
    else:
        click.echo(click.style("✗ Invalid DID syntax", fg='red'))
        sys.exit(1)


@cli.command()
@click.argument('did_file', type=click.Path(exists=True))
def verify_document(did_file):
    """
    Verify a DID document file is valid
    
    Example:
        payelink-agent-identity verify-document my-did.json
    """
    try:
        from ..sdk.types import DIDDocument
        
        content = Path(did_file).read_text()
        doc_data = json.loads(content)
        
        # Validate using Pydantic model
        document = DIDDocument(**doc_data)
        
        click.echo(click.style("✓ Valid DID document", fg='green'))
        click.echo(f"DID: {document.id}")
        
        if document.verificationMethod:
            click.echo(f"Verification methods: {len(document.verificationMethod)}")
        
        if document.service:
            click.echo(f"Services: {len(document.service)}")
        
    except Exception as e:
        click.echo(click.style(f"✗ Invalid DID document: {str(e)}", fg='red'), err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()
