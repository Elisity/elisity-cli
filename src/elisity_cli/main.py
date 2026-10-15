"""
Elisity CLI — main entry point.

Usage:
    elisity [OPTIONS] COMMAND [ARGS]...
"""

import click

from elisity_cli import __version__
from elisity_cli.config import get_active_profile
from elisity_cli.context import CliContext, pass_context


@click.group(context_settings={"allow_interspersed_args": False})
@click.version_option(version=__version__, prog_name="elisity")
@click.option("--format", "-f", "fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format (default: json)")
@click.option("--query", "-q", type=str, default=None, help="JMESPath query to filter output")
@click.option("--debug", is_flag=True, default=False, help="Enable debug logging (show HTTP requests)")
@click.option("--profile", "-p", type=str, default=None, help="Use a named profile from ~/.elisity/config.yaml")
@pass_context
def cli(ctx, fmt, query, debug, profile):
    """Elisity CCC CLI — command-line interface to the Cloud Control Center API.

    Manages topology, policies, devices, connectors, AD/Entra integration,
    traffic flows, and system operations — 658 commands across 12 groups
    (9 API-backed + 3 CLI-native: auth, config, glossary).

    Configuration:
      Set CCC_BASE_URL, CCC_CLIENT_ID, CCC_CLIENT_SECRET env vars, or
      run 'elisity config set-profile' to store credentials.

    Examples:
      elisity topology get-site-v2 <site-id>
      elisity devices get-devices-view --body '{"pageable":{"page":0,"size":10}}'
      elisity policy get-all-as-nd-json --format table
    """
    profile_data = get_active_profile()
    if profile:
        from elisity_cli.config import load_config
        config = load_config()
        profiles = config.get("profiles", {})
        if profile not in profiles:
            click.echo(f"Error: Profile '{profile}' not found.", err=True)
            raise SystemExit(1)
        profile_data = {**profile_data, **profiles[profile]}

    ctx.format = fmt or profile_data.get("default_format", "json")
    ctx.query = query
    ctx.debug = debug
    ctx.profile_data = profile_data


# --- Config commands (built-in, not generated) ---


@cli.group("config")
def config_group():
    """Manage CLI configuration — profiles, credentials, defaults."""
    pass


@config_group.command("set-profile")
@click.argument("name")
@click.option("--base-url", required=True, help="CCC base URL (e.g. https://ccc.example.elisity.io)")
@click.option("--client-id", required=True, help="OAuth2 client ID")
@click.option("--client-secret", required=True, help="OAuth2 client secret")
@click.option("--timeout", type=int, default=30, help="Request timeout in seconds")
@click.option("--default-format", type=click.Choice(["json", "table", "yaml", "csv"]), default="json")
def set_profile(name, base_url, client_id, client_secret, timeout, default_format):
    """Create or update a named connection profile."""
    from elisity_cli.config import set_profile as _set_profile
    _set_profile(name, base_url, client_id, client_secret, timeout=timeout, default_format=default_format)
    click.echo(f"Profile '{name}' saved to ~/.elisity/config.yaml")


@config_group.command("use-profile")
@click.argument("name")
def use_profile(name):
    """Switch the active profile."""
    from elisity_cli.config import use_profile as _use_profile
    try:
        _use_profile(name)
        click.echo(f"Switched to profile '{name}'")
    except ValueError as e:
        click.echo(str(e), err=True)
        raise SystemExit(1)


@config_group.command("list-profiles")
def list_profiles():
    """List all configured profiles."""
    from elisity_cli.config import list_profiles as _list_profiles
    from elisity_cli.output import render
    profiles = _list_profiles()
    if not profiles:
        click.echo("No profiles configured. Run 'elisity config set-profile <name> ...'")
        return
    render(profiles, "json")


@config_group.command("show")
@pass_context
def show_config(ctx):
    """Show the active connection configuration (secrets redacted)."""
    from elisity_cli.output import render
    p = ctx.profile_data or get_active_profile()
    safe = {k: ("***" if "secret" in k else v) for k, v in p.items()}
    render(safe, ctx.format)


# --- Auth commands ---


@cli.group("auth")
def auth_group():
    """Authentication operations — test connection, get token info."""
    pass


@auth_group.command("test")
@pass_context
def auth_test(ctx):
    """Test authentication against the CCC API."""
    from elisity_cli.output import render
    client = ctx.ensure_client()
    result = client.health_check()
    render(result, ctx.format, ctx.query)
    if result.get("status") != "healthy":
        raise SystemExit(1)


@auth_group.command("token")
@pass_context
def auth_token(ctx):
    """Get a fresh OAuth2 access token (for scripting)."""
    client = ctx.ensure_client()
    client._ensure_auth()
    click.echo(client.access_token)


@auth_group.command("whoami")
@pass_context
def auth_whoami(ctx):
    """Decode and display the current token claims."""
    import base64
    import json
    client = ctx.ensure_client()
    client._ensure_auth()
    token = client.access_token
    # Decode JWT payload (no verification — just display)
    parts = token.split(".")
    if len(parts) >= 2:
        payload = parts[1]
        # Add padding
        payload += "=" * (4 - len(payload) % 4)
        decoded = json.loads(base64.urlsafe_b64decode(payload))
        from elisity_cli.output import render
        render(decoded, ctx.format, ctx.query)
    else:
        click.echo("Could not decode token", err=True)
        raise SystemExit(1)


# --- Register auto-generated command groups ---

def _register_groups():
    """Import and register all auto-generated command groups."""
    from elisity_cli.commands import COMMAND_GROUPS
    for group_name in COMMAND_GROUPS:
        try:
            mod = __import__(f"elisity_cli.commands.{group_name}", fromlist=["group"])
            cli.add_command(mod.group)
        except Exception as e:
            # Don't crash the whole CLI if one group has issues
            click.echo(f"Warning: Failed to load '{group_name}' commands: {e}", err=True)


_register_groups()


if __name__ == "__main__":
    cli()
