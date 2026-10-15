"""
Active Directory / Entra ID integration — connectors, users, groups, agents

Auto-generated from the Elisity CCC OpenAPI specification.
"""

import click

from elisity_cli.context import CliContext, pass_context
from elisity_cli.output import render


@click.group("ad")
@pass_context
def group(ctx):
    """Active Directory / Entra ID integration — connectors, users, groups, agents"""
    pass

@group.command("get-groups-default-enabled")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_groups_default_enabled(ctx, cmd_fmt, cmd_query):
    """Get the 'enable all groups by default' toggle"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/groups/default-enabled"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("set-groups-default-enabled")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_set_groups_default_enabled(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Set the 'enable all groups by default' toggle (master reset)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/ad-connector-service/v1/groups/default-enabled"
    params = None
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("ping")
@click.argument("nodeid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_ping(ctx, nodeid, cmd_fmt, cmd_query):
    """Health check"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/connectors/{nodeid}/ping"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("set-distribution-zones")
@click.argument("nodeid")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_set_distribution_zones(ctx, nodeid, body_data, body_file, cmd_fmt, cmd_query):
    """Set distribution zones for a connector"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/connectors/{nodeid}/distribution-zones"
    params = None
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-configuration-value")
@click.option("--name", "name", type=str, required=True, help="<b>List of supported configuration names:</b> <br>sync.structure.chunk.size<br>u")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_configuration_value(ctx, name, cmd_fmt, cmd_query):
    """Get configuration value"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/configuration"
    params = {}
    if name is not None:
        params["name"] = name
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("put-configuration-value")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_put_configuration_value(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Update configuration value"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/configuration"
    params = None
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-activity-logs")
@click.option("--nodeId", "nodeId", type=str, default=None, help="Optional AD Agent node identifier. If omitted, events from all agents are return")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_activity_logs(ctx, nodeId, globalFilter, page, size, sort, cmd_fmt, cmd_query):
    """Query agent activity log"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v2/agent/activity"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("save-activity-logs")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_save_activity_logs(ctx, nodeId, body_data, body_file, cmd_fmt, cmd_query):
    """Receive activity log events from agent"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v2/agent/activity"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("export-users-logon-history")
@click.argument("deviceid")
@click.option("--from", "from_param", type=str, default=None, help="from")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export_users_logon_history(ctx, deviceid, from_param, body_data, body_file, cmd_fmt, cmd_query):
    """Generate users logon export as CSV"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/user/logon-history/{deviceid}/export"
    params = {}
    if from_param is not None:
        params["from"] = from_param
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("export-users")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export_users(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Generate users export as CSV"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/user/export"
    params = None
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("refresh-all-entra")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_refresh_all_entra(ctx, cmd_fmt, cmd_query):
    """Refresh all Entra subscriptions"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/refresh/entra"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("refresh-all-ad-on-prem")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_refresh_all_ad_on_prem(ctx, cmd_fmt, cmd_query):
    """Refresh all AD on-prem subscriptions"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/refresh/ad-onprem"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-groups-view")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_groups_view(ctx, globalFilter, page, size, sort, cmd_fmt, cmd_query):
    """Get groups view"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/groups"
    params = {}
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("set-groups-enabled")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_set_groups_enabled(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Enable or disable one or many groups"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/groups"
    params = None
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.patch(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-group-users")
@click.argument("id")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_group_users(ctx, id, globalFilter, page, size, sort, cmd_fmt, cmd_query):
    """Get users that are direct members of a group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/groups/{id}/users"
    params = {}
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-group-devices")
@click.argument("id")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_group_devices(ctx, id, globalFilter, page, size, sort, cmd_fmt, cmd_query):
    """Get devices that are direct members of a group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/groups/{id}/devices"
    params = {}
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("export-groups")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export_groups(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Generate groups export as XLSX"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/groups/export"
    params = None
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("sync")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_sync(ctx, cmd_fmt, cmd_query):
    """Sync Entra"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/entra/sync"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("export-users-post")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export_users_post(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Generate Entra users export as CSV"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/entra/export"
    params = None
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-auth")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_auth(ctx, cmd_fmt, cmd_query):
    """Get Entra authentication"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/entra/auth"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-auth")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_auth(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Update Entra authentication"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/entra/auth"
    params = None
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("delete-auth")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_auth(ctx, cmd_fmt, cmd_query, confirm):
    """Delete Entra authentication and all related data"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/ad-connector-service/v1/entra/auth"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-connectors")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_connectors(ctx, page, size, sort, cmd_fmt, cmd_query):
    """Get connectors"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/connectors"
    params = {}
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("register-connector")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_register_connector(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Register the connector"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/connectors"
    params = None
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("resync")
@click.argument("nodeid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_resync(ctx, nodeid, cmd_fmt, cmd_query):
    """Resync the connector"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/connectors/resync/{nodeid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("restart")
@click.argument("nodeid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_restart(ctx, nodeid, cmd_fmt, cmd_query):
    """Restart the connector"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/connectors/restart/{nodeid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("upload-logs")
@click.argument("nodeid")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_upload_logs(ctx, nodeid, body_data, body_file, cmd_fmt, cmd_query):
    """Upload agent logs"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/{nodeid}/logs"
    params = None
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-pull-status")
@click.argument("nodeid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_pull_status(ctx, nodeid, cmd_fmt, cmd_query):
    """Get the status of a previously-initiated log pull; on success streams the ZIP bytes"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/{nodeid}/logs/pull"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("pull-logs")
@click.argument("nodeid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_pull_logs(ctx, nodeid, cmd_fmt, cmd_query):
    """Initiate a log pull from an AD Agent"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/{nodeid}/logs/pull"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-agent-to-version")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--versionToUpdate", "versionToUpdate", type=str, default=None, help="Optionally, When given then upgrade agent to the specified version. Such value a")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_agent_to_version(ctx, nodeId, versionToUpdate, cmd_fmt, cmd_query):
    """Update AD Agent to specific or latest version"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/update"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    if versionToUpdate is not None:
        params["versionToUpdate"] = versionToUpdate
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-all-agents-to-latest-version")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_all_agents_to_latest_version(ctx, cmd_fmt, cmd_query):
    """Update all AD Agents to latest version"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/update-all"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("agent-status")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_agent_status(ctx, nodeId, body_data, body_file, cmd_fmt, cmd_query):
    """Set AD Agent and DC status"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/status"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("save-logger-change")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_save_logger_change(ctx, nodeId, body_data, body_file, cmd_fmt, cmd_query):
    """Save log level for specific AD Agent"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/logger"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("export")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Generate AD Agents export as CSV"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/export"
    params = None
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-agent-description")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_agent_description(ctx, nodeId, body_data, body_file, cmd_fmt, cmd_query):
    """Save AD Agent description"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/description"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-agent-service-credentials")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--version", "version", type=int, default=None, help="Optionally. When given then, if ADCS has a newer version, it will respond with t")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_agent_service_credentials(ctx, nodeId, version, cmd_fmt, cmd_query):
    """Get AD Agent service credentials"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/credentials"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    if version is not None:
        params["version"] = version
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-agent-service-credentials")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_agent_service_credentials(ctx, nodeId, body_data, body_file, cmd_fmt, cmd_query):
    """Save AD Agent service credentials"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/credentials"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-ad-agent-config")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--loggingVersion", "loggingVersion", type=int, default=None, help="Current logging version. If the provided loggingVersion parameter is the same or")
@click.option("--configVersion", "configVersion", type=int, default=None, help="Current config version. Returns null if it is equal to or greater than the versi")
@click.option("--syslogVersion", "syslogVersion", type=int, default=None, help="Current syslog version. If the provided syslogVersion parameter is the same or g")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_ad_agent_config(ctx, nodeId, loggingVersion, configVersion, syslogVersion, cmd_fmt, cmd_query):
    """Get config for specific AD Agent"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/config"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    if loggingVersion is not None:
        params["loggingVersion"] = loggingVersion
    if configVersion is not None:
        params["configVersion"] = configVersion
    if syslogVersion is not None:
        params["syslogVersion"] = syslogVersion
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("save-ad-agent-config")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_save_ad_agent_config(ctx, nodeId, body_data, body_file, cmd_fmt, cmd_query):
    """Save new config for specific AD Agent"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/config"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    body = None
    if body_file:
        import json as _json
        with open(body_file) as f:
            body = _json.load(f)
    elif body_data:
        import json as _json
        body = _json.loads(body_data)
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, data=body, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-dc-bookmark")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--hostname", "hostname", type=str, required=True, help="Domain Controller hostname")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_dc_bookmark(ctx, nodeId, hostname, cmd_fmt, cmd_query):
    """Get DC bookmark for specific AD Agent and DC hostname"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v2/agent/dc/bookmark"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    if hostname is not None:
        params["hostname"] = hostname
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-users-view")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_users_view(ctx, globalFilter, page, size, sort, cmd_fmt, cmd_query):
    """Get users view"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/user/view"
    params = {}
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-users-logon-history")
@click.argument("deviceid")
@click.option("--from", "from_param", type=str, required=True, help="Start time for the query (in ISO 8601 format). Only logon events occurring on or")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_users_logon_history(ctx, deviceid, from_param, globalFilter, page, size, sort, cmd_fmt, cmd_query):
    """Retrieve user logon history for a device"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/user/logon-history/{deviceid}"
    params = {}
    if from_param is not None:
        params["from"] = from_param
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-users-count-data")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_users_count_data(ctx, cmd_fmt, cmd_query):
    """Get users count"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/user/count"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-suppressed-ip-attaches")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_suppressed_ip_attaches(ctx, cmd_fmt, cmd_query):
    """Get all suppressed IP attaches"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/ip-attach/suppressed"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-groups-count")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_groups_count(ctx, cmd_fmt, cmd_query):
    """Get groups count"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/groups/count"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-entra-users")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_entra_users(ctx, globalFilter, page, size, sort, cmd_fmt, cmd_query):
    """Entra users"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/entra/view"
    params = {}
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("status")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_status(ctx, cmd_fmt, cmd_query):
    """Entra status"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/entra/status"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-isolated-distribution-zones")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_isolated_distribution_zones(ctx, cmd_fmt, cmd_query):
    """GET /api/ad-connector-service/v1/distribution-zones"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/distribution-zones"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-connector-by-id")
@click.argument("nodeid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_connector_by_id(ctx, nodeid, cmd_fmt, cmd_query):
    """Get the connector"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/connectors/{nodeid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("unregister-connector")
@click.argument("nodeid")
@click.option("--deleteAdData", "deleteAdData", type=bool, default=False, help="When true, also delete all AD data (users, devices) for the connector's domain i")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_unregister_connector(ctx, nodeid, deleteAdData, cmd_fmt, cmd_query, confirm):
    """Unregister the connector"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/ad-connector-service/v1/connectors/{nodeid}"
    params = {}
    if deleteAdData is not None:
        params["deleteAdData"] = deleteAdData
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-connector-deletion-context")
@click.argument("nodeid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_connector_deletion_context(ctx, nodeid, cmd_fmt, cmd_query):
    """Get connector deletion context"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/connectors/{nodeid}/deletion-context"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-distribution-zone-assignments")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_distribution_zone_assignments(ctx, cmd_fmt, cmd_query):
    """Get distribution zone assignments per connector"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/connectors/distribution-zone-assignments"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-attribute-values")
@click.option("--id", "id", type=str, required=True, help="<b>List of supported IDs:</b> <br>ad.deviceAccountId<br>ad.dn<br>ad.deviceGroups")
@click.option("--searchText", "searchText", type=str, default=None, help="searchText")
@click.option("--page", "page", type=int, default=0, help="page")
@click.option("--size", "size", type=int, default=200, help="size")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_attribute_values(ctx, id, searchText, page, size, cmd_fmt, cmd_query):
    """Get attribute values"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/attribute"
    params = {}
    if id is not None:
        params["id"] = id
    if searchText is not None:
        params["searchText"] = searchText
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-agents-and-dcs")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_agents_and_dcs(ctx, globalFilter, page, size, sort, cmd_fmt, cmd_query):
    """Get list of AD Agents and DCs"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent"
    params = {}
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("agent-manifest")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--revision", "revision", type=int, required=True, help="revision number of agent manifest. If the version is greater than requested it w")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_agent_manifest(ctx, nodeId, revision, cmd_fmt, cmd_query):
    """Get AD Agent version manifest"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/manifest"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    if revision is not None:
        params["revision"] = revision
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-connectors-get")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_connectors_get(ctx, cmd_fmt, cmd_query):
    """Get loggers for all active AD Agents"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/logging"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-syslog-credentials")
@click.option("--nodeId", "nodeId", type=str, required=True, help="AD Agent node identifier")
@click.option("--version", "version", type=int, default=None, help="Optional. When given, if ADCS has a newer version it responds with the updated c")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_syslog_credentials(ctx, nodeId, version, cmd_fmt, cmd_query):
    """Get syslog credentials"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/ad-connector-service/v1/agent/credentials/syslog"
    params = {}
    if nodeId is not None:
        params["nodeId"] = nodeId
    if version is not None:
        params["version"] = version
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)
