"""
Manage network topology — sites, zones, VE groups, VEs, VENs, flow exporters

Auto-generated from the Elisity CCC OpenAPI specification.
"""

import click

from elisity_cli.context import CliContext, pass_context
from elisity_cli.output import render


@click.group("topology")
@pass_context
def group(ctx):
    """Manage network topology — sites, zones, VE groups, VEs, VENs, flow exporters"""
    pass

@group.command("list-workload-distribution-zones")
@click.option("--id", "id", type=str, default=None, help="Optional filter — matches either the zone's numericId or its UUID")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_workload_distribution_zones(ctx, id, cmd_fmt, cmd_query):
    """List Workload Distribution Zones known to Identity Graph"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/workload-distribution-zones"
    params = {}
    if id is not None:
        params["id"] = id
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-workload-distribution-zone-usage")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_workload_distribution_zone_usage(ctx, id, cmd_fmt, cmd_query):
    """Report whether a Workload Distribution Zone is referenced by any workload-discovery connector endpoint"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/workload-distribution-zones/{id}/usage"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-site-v2")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_site_v2(ctx, id, cmd_fmt, cmd_query):
    """Get single Site"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/sites/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-site")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_site(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update site"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/sites/{id}"
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

@group.command("delete-site-v2")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_site_v2(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete site"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v2/sites/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-virtual-edge-by-id")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edge_by_id(ctx, id, cmd_fmt, cmd_query):
    """Get a virtual edge by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-virtual-edge")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_virtual_edge(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update existing virtual edge"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}"
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

@group.command("delete-virtual-edge")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_virtual_edge(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete existing virtual edge"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/virtual-edges/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-virtual-edge-put")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_virtual_edge_put(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Override OTP for existing virtual edge"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/otp"
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

@group.command("update-virtual-edge-post")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_virtual_edge_post(ctx, id, cmd_fmt, cmd_query):
    """Regenerate OTP for existing virtual edge"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/otp"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-manifest")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_manifest(ctx, id, cmd_fmt, cmd_query):
    """Get manifest with versions for Central VE"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/manifest"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("set-version")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_set_version(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Set desired version in manifest of Central VE for nodeId"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/manifest"
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

@group.command("change-virtual-edge-group")
@click.argument("id")
@click.argument("idnewvirtualedgegroup")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_change_virtual_edge_group(ctx, id, idnewvirtualedgegroup, cmd_fmt, cmd_query):
    """Change virtual edge group for existing virtual edge"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/change-group/{idnewvirtualedgegroup}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("ack-registration")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_ack_registration(ctx, id, cmd_fmt, cmd_query):
    """Acknowledge registration of Central VE"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/ack"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-single-ven")
@click.argument("id")
@click.option("--expands", "expands", type=str, default=None, help="Optional field expansion to include additional data. Use 'topology' for all neig")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_single_ven(ctx, id, expands, cmd_fmt, cmd_query):
    """Get single Virtual Edge Node"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}"
    params = {}
    if expands is not None:
        params["expands"] = expands
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-ven")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_ven(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update existing virtual edge node"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}"
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

@group.command("delete-ven")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_ven(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete virtual edge node"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("exclude-adjacent-vens")
@click.argument("id")
@click.argument("visibilityvenid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_exclude_adjacent_vens(ctx, id, visibilityvenid, cmd_fmt, cmd_query):
    """Exclude adjacent VEN from topology"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/topology/exclude/{visibilityvenid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("rediscover-adjacent-vens")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_rediscover_adjacent_vens(ctx, id, cmd_fmt, cmd_query):
    """Rediscover adjacent VENs and recreate missing ones"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/topology/discover"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("re-initialize-virtual-edge-node")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_re_initialize_virtual_edge_node(ctx, id, cmd_fmt, cmd_query):
    """Trigger re-initialization of a unsuccessful recommission or onboard"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/reinitialize"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("recommission-virtual-edge-node")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_recommission_virtual_edge_node(ctx, id, cmd_fmt, cmd_query):
    """Trigger recommission of a decommissioned virtual edge node"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/recommission"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-ports-configuration")
@click.argument("id")
@click.argument("type_param")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_ports_configuration(ctx, id, type_param, cmd_fmt, cmd_query):
    """Get ports configuration for a VEN"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/ports-configuration/{type_param}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-ports-configuration")
@click.argument("id")
@click.argument("type_param")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_ports_configuration(ctx, id, type_param, body_data, body_file, cmd_fmt, cmd_query):
    """Update ports configuration for a VEN"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/ports-configuration/{type_param}"
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

@group.command("decommission-virtual-edge-node")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_decommission_virtual_edge_node(ctx, id, cmd_fmt, cmd_query, confirm):
    """Trigger decommission of a registered virtual edge node"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/decommission"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("change-ven-group")
@click.argument("id")
@click.argument("newvirtualedgegroupid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_change_ven_group(ctx, id, newvirtualedgegroupid, cmd_fmt, cmd_query):
    """Change Virtual Edge Group for a Virtual Edge Node (VEN)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/change-group/{newvirtualedgegroupid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("change-active-ve")
@click.argument("id")
@click.argument("targetveid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_change_active_ve(ctx, id, targetveid, cmd_fmt, cmd_query):
    """Change Active Virtual Edge for a Virtual Edge Node (VEN)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/change-active-ve/{targetveid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("validate-virtual-edge-nodes-bulk-update")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_virtual_edge_nodes_bulk_update(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Bulk update VEN credentials"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/bulk"
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

@group.command("get-virtual-edge-group-by-id")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edge_group_by_id(ctx, id, cmd_fmt, cmd_query):
    """Get a virtual edge group by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-groups/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-virtual-edge-group")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_virtual_edge_group(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update existing virtual edge group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-groups/{id}"
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

@group.command("delete-virtual-edge-group")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_virtual_edge_group(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete existing virtual edge group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/virtual-edge-groups/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("patch-virtual-edge-group")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_patch_virtual_edge_group(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Partial-update of a virtual edge group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-groups/{id}"
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

@group.command("rebalance-virtual-edge-group")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_rebalance_virtual_edge_group(ctx, id, cmd_fmt, cmd_query):
    """Rebalance Virtual Edge Group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-groups/{id}/rebalance"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-task-list")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_task_list(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update a task list"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/task-list/{id}"
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

@group.command("update-task-status")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_task_status(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update task status report"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/task-list/{id}/report"
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

@group.command("update-target-site-by-id")
@click.argument("type_param")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_target_site_by_id(ctx, type_param, id, body_data, body_file, cmd_fmt, cmd_query):
    """Updates an existing target site entry by ID (for active or future entries)."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/targets/{type_param}/{id}"
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

@group.command("get-all-sites")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_sites(ctx, cmd_fmt, cmd_query):
    """Get all Sites"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/sites"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-site-put")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_site_put(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Update site."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/sites"
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

@group.command("create-site")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_site(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create list of sites."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/sites"
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

@group.command("get-site")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_site(ctx, id, cmd_fmt, cmd_query):
    """Get single Site"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/sites/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-site-put-2")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_site_put_2(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update site."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/sites/{id}"
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

@group.command("delete-site")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_site(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete site."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/sites/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-settings")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_settings(ctx, cmd_fmt, cmd_query):
    """Get topology settings"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/settings"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-settings")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_settings(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Update topology settings"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/settings"
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

@group.command("get-global-interfaces-settings")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_global_interfaces_settings(ctx, cmd_fmt, cmd_query):
    """Get global interface settings"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/interfaces-settings"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-global-interfaces-settings")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_global_interfaces_settings(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Update global interface settings"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/interfaces-settings"
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

@group.command("update-interfaces-settings")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_interfaces_settings(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update interface settings by ID (deprecated)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/interfaces-settings/{id}"
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

@group.command("update-global-credentials")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_global_credentials(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update global credentials"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/global-credentials/{id}"
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

@group.command("delete-global-credentials")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_global_credentials(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete global credentials"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/global-credentials/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-flow-exporter")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_flow_exporter(ctx, id, cmd_fmt, cmd_query):
    """Get a single flow exporter"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/flow-exporters/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-flow-exporter")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_flow_exporter(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update a flow exporter"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/flow-exporters/{id}"
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

@group.command("delete-flow-exporter")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_flow_exporter(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete a flow exporter"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/flow-exporters/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-all-distribution-zones")
@click.option("--includeIsolated", "includeIsolated", type=bool, default=False, help="When `true`, Isolated Distribution Zones are included in the response. Isolated ")
@click.option("--includeWorkload", "includeWorkload", type=bool, default=False, help="When `true`, Workload Distribution Zones are included in the response. Workload ")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_distribution_zones(ctx, includeIsolated, includeWorkload, cmd_fmt, cmd_query):
    """Get all Distribution Zones"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/distribution-zones"
    params = {}
    if includeIsolated is not None:
        params["includeIsolated"] = includeIsolated
    if includeWorkload is not None:
        params["includeWorkload"] = includeWorkload
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-distribution-zone")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_distribution_zone(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Update Distribution Zone"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/distribution-zones"
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

@group.command("create-distribution-zone")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_distribution_zone(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create Distribution Zones"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/distribution-zones"
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

@group.command("update-cloud-controller")
@click.argument("id")
@click.option("--cloudType", "cloudType", type=str, required=True, help="Type of cloud controller")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_cloud_controller(ctx, id, cloudType, body_data, body_file, cmd_fmt, cmd_query):
    """Update cloud controller"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/cloud-controller/{id}"
    params = {}
    if cloudType is not None:
        params["cloudType"] = cloudType
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

@group.command("delete-cloud-controller")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_cloud_controller(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete Mist cloud controller"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/cloud-controller/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("validate-virtual-edges-bulk-json")
@click.option("--virtualEdgeType", "virtualEdgeType", type=str, required=True, help="Type of Virtual Edge to create from the file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_virtual_edges_bulk_json(ctx, virtualEdgeType, cmd_fmt, cmd_query):
    """Validate VE rows for bulk upload (V2, JSON streaming)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edges/bulk/validate"
    params = {}
    if virtualEdgeType is not None:
        params["virtualEdgeType"] = virtualEdgeType
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("upload-virtual-edges-bulk-json")
@click.option("--virtualEdgeType", "virtualEdgeType", type=str, required=True, help="Type of Virtual Edge to create")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_upload_virtual_edges_bulk_json(ctx, virtualEdgeType, cmd_fmt, cmd_query):
    """Bulk upload VE rows (V2, JSON streaming)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edges/bulk/upload"
    params = {}
    if virtualEdgeType is not None:
        params["virtualEdgeType"] = virtualEdgeType
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("search-virtual-edge-nodes")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_search_virtual_edge_nodes(ctx, page, size, sort, body_data, body_file, cmd_fmt, cmd_query):
    """List Virtual Edge Nodes with pagination and sorting"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edge-nodes/search"
    params = {}
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
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

@group.command("get-virtual-edge-nodes-metrics-summary")
@click.option("--dimensions", "dimensions", type=str, default=None, help="Comma-separated dimension keys to compute; defaults to all registered dimensions")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edge_nodes_metrics_summary(ctx, dimensions, body_data, body_file, cmd_fmt, cmd_query):
    """Aggregated VEN counts grouped per dimension (metrics summary)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edge-nodes/metrics/summary"
    params = {}
    if dimensions is not None:
        params["dimensions"] = dimensions
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

@group.command("validate-virtual-edge-nodes-bulk-json")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_virtual_edge_nodes_bulk_json(ctx, cmd_fmt, cmd_query):
    """Validate VEN rows for bulk upload (V2, JSON streaming)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edge-nodes/bulk/validate"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("upload-virtual-edge-nodes-bulk-json")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_upload_virtual_edge_nodes_bulk_json(ctx, cmd_fmt, cmd_query):
    """Bulk upload VEN rows (V2, JSON streaming)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edge-nodes/bulk/upload"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-all-sites-v2")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter — searches across label, description, tags, createdBy, and modifie")
@click.option("--columnFilters", "columnFilters", type=str, default=None, help="Column-specific filter in the format: columnFilters=attributeName,keyword,value.")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_sites_v2(ctx, globalFilter, columnFilters, sort, page, size, cmd_fmt, cmd_query):
    """Get all Sites (paginated)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/sites"
    params = {}
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if columnFilters is not None:
        params["columnFilters"] = columnFilters
    if sort is not None:
        params["sort"] = sort
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

@group.command("create-site-post")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_site_post(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create site label"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/sites"
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

@group.command("get-site-label-independent-control-mappings")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_site_label_independent_control_mappings(ctx, cmd_fmt, cmd_query):
    """Get all Independent Control Mappings for Site Labels"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/sites/independent-control-mappings"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("create-site-label-independent-control-mappings")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_site_label_independent_control_mappings(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create Independent Control Mappings between Site Labels"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/sites/independent-control-mappings"
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

@group.command("delete-site-label-independent-control-mappings")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_site_label_independent_control_mappings(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Delete Independent Control Mappings for Site Labels"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v2/sites/independent-control-mappings"
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
        result = client.delete(endpoint, params=params, data=body)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("export-site-labels")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export_site_labels(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Export site labels as CSV"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/sites/export"
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

@group.command("bulk-create-site-labels")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_bulk_create_site_labels(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Bulk create site labels"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/sites/bulk"
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

@group.command("bulk-delete-site-v2")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_bulk_delete_site_v2(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Bulk delete site labels"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v2/sites/bulk/delete"
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

@group.command("export-distribution-zones")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export_distribution_zones(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Export Distribution Zones as CSV"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/distribution-zones/export"
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

@group.command("get-virtual-edge")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--columnFilters", "columnFilters", type=str, default=None, help="Filtering criteria in the format: columnFilters=attributeName,keyword,value&colu")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edge(ctx, sort, globalFilter, columnFilters, page, size, cmd_fmt, cmd_query):
    """Search and filter virtual edge"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges"
    params = {}
    if sort is not None:
        params["sort"] = sort
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if columnFilters is not None:
        params["columnFilters"] = columnFilters
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

@group.command("create-virtual-edge")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_virtual_edge(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create new virtual edge"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges"
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

@group.command("get-ve-variables")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_ve_variables(ctx, id, cmd_fmt, cmd_query):
    """Download variables for a VE"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/variables"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("publish-ve-variables")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_publish_ve_variables(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Publish variables for a VE"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/variables"
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

@group.command("metrics")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_metrics(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Publish operational metrics for a VE"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/metrics"
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

@group.command("enable-maintenance")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_enable_maintenance(ctx, id, cmd_fmt, cmd_query):
    """Enable Maintenance mode on a Virtual Edge"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/maintenance/enable"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("disable-maintenance")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_disable_maintenance(ctx, id, cmd_fmt, cmd_query):
    """Disable Maintenance mode on a Virtual Edge"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/maintenance/disable"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("heartbeat")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_heartbeat(ctx, id, cmd_fmt, cmd_query):
    """Register heartbeat for a VE"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/{id}/heartbeat"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-virtual-edge-by-post")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edge_by_post(ctx, sort, page, size, body_data, body_file, cmd_fmt, cmd_query):
    """Search and filter virtual edge"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/view"
    params = {}
    if sort is not None:
        params["sort"] = sort
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
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

@group.command("register")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_register(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Register a VE"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/register"
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

@group.command("get-virtual-edges-metrics-summary")
@click.option("--dimensions", "dimensions", type=str, default=None, help="Comma-separated dimension keys to compute; defaults to every registered dimensio")
@click.option("--topN", "topN", type=int, default=5, help="Highlight list size for dimensions that have one (1..100)")
@click.option("--versionFloor", "versionFloor", type=str, default=None, help="Lowest supported version (computed by the FE) — required when the upgradeStatus ")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edges_metrics_summary(ctx, dimensions, topN, versionFloor, body_data, body_file, cmd_fmt, cmd_query):
    """Aggregated VE counts grouped per dimension (metrics summary)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/metrics/summary"
    params = {}
    if dimensions is not None:
        params["dimensions"] = dimensions
    if topN is not None:
        params["topN"] = topN
    if versionFloor is not None:
        params["versionFloor"] = versionFloor
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

@group.command("get-logger")
@click.argument("loggername")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_logger(ctx, loggername, cmd_fmt, cmd_query):
    """Get logger level"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/loggers/{loggername}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("set-logger-level")
@click.argument("loggername")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_set_logger_level(ctx, loggername, body_data, body_file, cmd_fmt, cmd_query):
    """Set logger level"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/loggers/{loggername}"
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

@group.command("use-default-logger-level")
@click.argument("loggername")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_use_default_logger_level(ctx, loggername, cmd_fmt, cmd_query, confirm):
    """Reset logger to default level"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/virtual-edges/loggers/{loggername}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("set-logger-levels-bulk")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_set_logger_levels_bulk(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Set logger levels in bulk"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/loggers/bulk"
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

@group.command("export-virtual-edges")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export_virtual_edges(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Generate all virtual edges as XLSX"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/export"
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

@group.command("validate-virtual-edge-bulk-upload")
@click.option("--virtualEdgeType", "virtualEdgeType", type=str, required=True, help="Type of Virtual Edge to create from the file")
@click.option("--hostingMode", "hostingMode", type=str, required=True, help="Hosting mode for the Virtual Edges")
@click.option("--virtualEdgeGroupId", "virtualEdgeGroupId", type=str, default=None, help="Virtual Edge Group (VEG) UUID. Required when hosting mode is HYPERVISOR")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_virtual_edge_bulk_upload(ctx, virtualEdgeType, hostingMode, virtualEdgeGroupId, body_data, body_file, cmd_fmt, cmd_query):
    """Validate XLSX file for Virtual Edge bulk upload"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/bulk/validate"
    params = {}
    if virtualEdgeType is not None:
        params["virtualEdgeType"] = virtualEdgeType
    if hostingMode is not None:
        params["hostingMode"] = hostingMode
    if virtualEdgeGroupId is not None:
        params["virtualEdgeGroupId"] = virtualEdgeGroupId
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

@group.command("virtual-edge-bulk-upload")
@click.option("--virtualEdgeType", "virtualEdgeType", type=str, required=True, help="Type of Virtual Edge to create")
@click.option("--hostingMode", "hostingMode", type=str, required=True, help="Hosting mode for the Virtual Edges")
@click.option("--virtualEdgeGroupId", "virtualEdgeGroupId", type=str, default=None, help="Virtual Edge Group (VEG) UUID. Required when hosting mode is HYPERVISOR")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_virtual_edge_bulk_upload(ctx, virtualEdgeType, hostingMode, virtualEdgeGroupId, body_data, body_file, cmd_fmt, cmd_query):
    """Bulk upload Virtual Edges from XLSX file"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/bulk/upload"
    params = {}
    if virtualEdgeType is not None:
        params["virtualEdgeType"] = virtualEdgeType
    if hostingMode is not None:
        params["hostingMode"] = hostingMode
    if virtualEdgeGroupId is not None:
        params["virtualEdgeGroupId"] = virtualEdgeGroupId
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

@group.command("bulk-delete-virtual-edges")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_bulk_delete_virtual_edges(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Bulk delete Virtual Edges"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/virtual-edges/bulk/delete"
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

@group.command("validate-virtual-edge-bulk-delete")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_virtual_edge_bulk_delete(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Validate Virtual Edges before bulk delete"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/bulk/delete/validate"
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

@group.command("virtual-edge-bulk-change-group")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_virtual_edge_bulk_change_group(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Bulk change Virtual Edge group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/bulk/change-group"
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

@group.command("get-virtual-edge-nodes")
@click.option("--expands", "expands", type=str, default=None, help="expands")
@click.option("--contextVeId", "contextVeId", type=str, default=None, help="contextVeId")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--columnFilters", "columnFilters", type=str, default=None, help="Filtering criteria in the format: columnFilters=attributeName,keyword,value&colu")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edge_nodes(ctx, expands, contextVeId, globalFilter, columnFilters, page, size, sort, cmd_fmt, cmd_query):
    """List Virtual Edge Nodes with pagination and sorting"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes"
    params = {}
    if expands is not None:
        params["expands"] = expands
    if contextVeId is not None:
        params["contextVeId"] = contextVeId
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if columnFilters is not None:
        params["columnFilters"] = columnFilters
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

@group.command("create-ven")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_ven(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create a new virtual edge node"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes"
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

@group.command("get-topology")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_topology(ctx, id, cmd_fmt, cmd_query):
    """Get topology for a VEN"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/topology"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("topology")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_topology(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Publish topology seen from a VEN"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/topology"
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

@group.command("sxp-password-regenerate")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_sxp_password_regenerate(ctx, id, cmd_fmt, cmd_query):
    """Regenerate SXP password for Virtual Edge Node"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/sxp-password-regenerate"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("register-ven")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_register_ven(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Register virtual edge node"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/register"
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

@group.command("metrics-post")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_metrics_post(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Publish operational metrics for a VEN"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/metrics"
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

@group.command("heartbeat-post")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_heartbeat_post(ctx, id, cmd_fmt, cmd_query):
    """Register heartbeat from virtual edge node"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/heartbeat"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("create-or-update-multiple-rules")
@click.argument("id")
@click.argument("serialnumber")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_or_update_multiple_rules(ctx, id, serialnumber, body_data, body_file, cmd_fmt, cmd_query):
    """Create or update rules for given Palo Alto VEN and Firewall"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/firewalls/{serialnumber}/firewall-rules"
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

@group.command("batch-create-or-update-multiple-rules")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_batch_create_or_update_multiple_rules(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Bulk create or update rules for given Palo Alto VEN and Firewall"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/firewall-rules/batch"
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

@group.command("get-virtual-edge-nodes-by-post")
@click.option("--expands", "expands", type=str, default=None, help="expands")
@click.option("--contextVeId", "contextVeId", type=str, default=None, help="contextVeId")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edge_nodes_by_post(ctx, expands, contextVeId, page, size, sort, body_data, body_file, cmd_fmt, cmd_query):
    """List Virtual Edge Nodes with pagination and sorting"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/view"
    params = {}
    if expands is not None:
        params["expands"] = expands
    if contextVeId is not None:
        params["contextVeId"] = contextVeId
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
    if sort is not None:
        params["sort"] = sort
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

@group.command("export-virtual-edge-nodes")
@click.option("--contextVeId", "contextVeId", type=str, default=None, help="contextVeId")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export_virtual_edge_nodes(ctx, contextVeId, body_data, body_file, cmd_fmt, cmd_query):
    """Generate all virtual edge nodes as XLSX"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/export"
    params = {}
    if contextVeId is not None:
        params["contextVeId"] = contextVeId
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

@group.command("validate-virtual-edge-nodes-bulk-upload")
@click.option("--credentialMode", "credentialMode", type=str, required=True, help="Credential mode for the Virtual Edge Nodes")
@click.option("--globalCredentialId", "globalCredentialId", type=str, default=None, help="UUID of the global credential. Required when credentialMode is GLOBAL")
@click.option("--parentType", "parentType", type=str, required=True, help="Specifies whether VENs are assigned to a VE or a VE Group")
@click.option("--parentId", "parentId", type=str, required=True, help="UUID of the parent Virtual Edge or Virtual Edge Group, depending on parentType")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_virtual_edge_nodes_bulk_upload(ctx, credentialMode, globalCredentialId, parentType, parentId, body_data, body_file, cmd_fmt, cmd_query):
    """Validate XLSX file for Virtual Edge Node bulk upload"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/bulk/validate"
    params = {}
    if credentialMode is not None:
        params["credentialMode"] = credentialMode
    if globalCredentialId is not None:
        params["globalCredentialId"] = globalCredentialId
    if parentType is not None:
        params["parentType"] = parentType
    if parentId is not None:
        params["parentId"] = parentId
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

@group.command("virtual-edge-node-bulk-upload")
@click.option("--credentialMode", "credentialMode", type=str, required=True, help="Credential mode for the Virtual Edge Nodes")
@click.option("--globalCredentialId", "globalCredentialId", type=str, default=None, help="UUID of the global credential. Required when credentialMode is GLOBAL")
@click.option("--parentType", "parentType", type=str, required=True, help="Specifies whether VENs are assigned to a VE or a VE Group")
@click.option("--parentId", "parentId", type=str, required=True, help="UUID of the parent Virtual Edge or Virtual Edge Group, depending on parentType")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_virtual_edge_node_bulk_upload(ctx, credentialMode, globalCredentialId, parentType, parentId, body_data, body_file, cmd_fmt, cmd_query):
    """Bulk upload Virtual Edge Nodes from XLSX file"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/bulk/upload"
    params = {}
    if credentialMode is not None:
        params["credentialMode"] = credentialMode
    if globalCredentialId is not None:
        params["globalCredentialId"] = globalCredentialId
    if parentType is not None:
        params["parentType"] = parentType
    if parentId is not None:
        params["parentId"] = parentId
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

@group.command("bulk-recommission-ve-ns")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_bulk_recommission_ve_ns(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Bulk recommission Virtual Edge Nodes"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/bulk/recommission"
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

@group.command("bulk-force-delete-ve-ns")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_bulk_force_delete_ve_ns(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Bulk force delete Virtual Edge Nodes"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/virtual-edge-nodes/bulk/force-delete"
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

@group.command("bulk-delete-ve-ns")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_bulk_delete_ve_ns(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Bulk delete Virtual Edge Nodes"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/virtual-edge-nodes/bulk/delete"
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

@group.command("validate-virtual-edge-node-bulk-delete")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_virtual_edge_node_bulk_delete(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Validate Virtual Edge Nodes before bulk delete"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/bulk/delete/validate"
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

@group.command("bulk-change-ven-group")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_bulk_change_ven_group(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Bulk change Virtual Edge Group for multiple VENs"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/bulk/change-group"
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

@group.command("get-virtual-edge-get")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--columnFilters", "columnFilters", type=str, default=None, help="Filtering criteria in the format: columnFilters=attributeName,keyword,value&colu")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edge_get(ctx, sort, globalFilter, columnFilters, page, size, cmd_fmt, cmd_query):
    """Search and filter Virtual Edge Group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-groups"
    params = {}
    if sort is not None:
        params["sort"] = sort
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if columnFilters is not None:
        params["columnFilters"] = columnFilters
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

@group.command("create-virtual-edge-group")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_virtual_edge_group(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create new virtual edge group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-groups"
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

@group.command("enable-maintenance-for-group")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_enable_maintenance_for_group(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Enable Maintenance mode on a batch of Virtual Edges in a group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-groups/{id}/maintenance/enable"
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

@group.command("disable-maintenance-for-group")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_disable_maintenance_for_group(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Disable Maintenance mode on a batch of Virtual Edges in a group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-groups/{id}/maintenance/disable"
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

@group.command("get-virtual-edge-by-post-post")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edge_by_post_post(ctx, sort, page, size, body_data, body_file, cmd_fmt, cmd_query):
    """Search and filter virtual edge group"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-groups/view"
    params = {}
    if sort is not None:
        params["sort"] = sort
    if page is not None:
        params["page"] = page
    if size is not None:
        params["size"] = size
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

@group.command("create-task-list")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_task_list(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create a task list"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/task-list"
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

@group.command("get-all-target-sites")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_target_sites(ctx, cmd_fmt, cmd_query):
    """Get all configured deployment targets"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/targets"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("create-or-update-bulk-target-site")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_or_update_bulk_target_site(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Bulk create or update targets"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/targets"
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

@group.command("get-target-site")
@click.argument("type_param")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_target_site(ctx, type_param, cmd_fmt, cmd_query):
    """Get target for a specific type"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/targets/{type_param}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("create-or-update-target-site")
@click.argument("type_param")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_or_update_target_site(ctx, type_param, body_data, body_file, cmd_fmt, cmd_query):
    """Create or update target for a specific type"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/targets/{type_param}"
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

@group.command("delete-target-site")
@click.argument("type_param")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_target_site(ctx, type_param, cmd_fmt, cmd_query, confirm):
    """Delete target for a specific type"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/targets/{type_param}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("bulk-delete-site")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_bulk_delete_site(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Bulk delete site labels."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/sites/bulk/delete"
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

@group.command("get-all-global-credentials")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_global_credentials(ctx, cmd_fmt, cmd_query):
    """Get all global credentials"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/global-credentials"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("create-global-credentials")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_global_credentials(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create new global credentials"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/global-credentials"
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

@group.command("get-all-flow-exporter")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_flow_exporter(ctx, cmd_fmt, cmd_query):
    """Get all flow exporters"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/flow-exporters"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("create-flow-exporter")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_flow_exporter(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create a flow exporter"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/flow-exporters"
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

@group.command("get-independent-control-mappings")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_independent_control_mappings(ctx, cmd_fmt, cmd_query):
    """Get all Independent Control Mappings for Distribution Zones"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/distribution-zones/independent-control-mappings"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("create-independent-control-mappings")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_independent_control_mappings(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create Independent Control Mappings between Distribution Zones"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/distribution-zones/independent-control-mappings"
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

@group.command("delete-independent-control-mappings")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_independent_control_mappings(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Delete Independent Control Mappings"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/distribution-zones/independent-control-mappings"
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
        result = client.delete(endpoint, params=params, data=body)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("bulk-delete-distribution-zone")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_bulk_delete_distribution_zone(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Bulk delete Distribution Zones"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/distribution-zones/bulk/delete"
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

@group.command("get-dashboard-metrics")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_dashboard_metrics(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Get VE and VEN dashboard metrics"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/dashboard"
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

@group.command("get-all-cloud-controllers")
@click.option("--cloudType", "cloudType", type=str, required=True, help="Type of cloud controllers to retrieve")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_cloud_controllers(ctx, cloudType, cmd_fmt, cmd_query):
    """Get cloud controllers"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/cloud-controller"
    params = {}
    if cloudType is not None:
        params["cloudType"] = cloudType
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("create-cloud-controller")
@click.option("--cloudType", "cloudType", type=str, required=True, help="Type of cloud controller to create")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_cloud_controller(ctx, cloudType, body_data, body_file, cmd_fmt, cmd_query):
    """Create a new cloud controller"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/cloud-controller"
    params = {}
    if cloudType is not None:
        params["cloudType"] = cloudType
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

@group.command("get-reconciled-variables")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_reconciled_variables(ctx, id, cmd_fmt, cmd_query):
    """Reconciled environment variables for a VE"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edges/{id}/variables"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-status")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_status(ctx, id, cmd_fmt, cmd_query):
    """Get VEN status"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edge-nodes/{id}/status"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-permissions")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_permissions(ctx, id, cmd_fmt, cmd_query):
    """Get VEN permissions"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edge-nodes/{id}/permissions"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-metrics")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_metrics(ctx, id, cmd_fmt, cmd_query):
    """Get VEN metrics"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edge-nodes/{id}/metrics"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-details")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_details(ctx, id, cmd_fmt, cmd_query):
    """Get VEN details"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edge-nodes/{id}/details"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-configuration")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_configuration(ctx, id, cmd_fmt, cmd_query):
    """Get VEN configuration"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/virtual-edge-nodes/{id}/configuration"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-all-tags")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_tags(ctx, cmd_fmt, cmd_query):
    """Get all Tags used for Site Labels"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/sites/tags"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-site-count-v2")
@click.option("--durationInHours", "durationInHours", type=int, required=True, help="Number of hours to look back for 'new' sites. Must be between 0 and 24.")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_site_count_v2(ctx, durationInHours, cmd_fmt, cmd_query):
    """Get site count"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/sites/count"
    params = {}
    if durationInHours is not None:
        params["durationInHours"] = durationInHours
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-all-distribution-zones-get")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter — searches across name, description, type, createdBy, and modified")
@click.option("--columnFilters", "columnFilters", type=str, default=None, help="Column-specific filter in the format: columnFilters=attributeName,keyword,value.")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_distribution_zones_get(ctx, globalFilter, columnFilters, sort, page, size, cmd_fmt, cmd_query):
    """Get all Distribution Zones (paginated)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/distribution-zones"
    params = {}
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if columnFilters is not None:
        params["columnFilters"] = columnFilters
    if sort is not None:
        params["sort"] = sort
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

@group.command("get-virtual-edge-nodes-for-distribution-zone")
@click.argument("id")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--columnFilters", "columnFilters", type=str, default=None, help="Filtering criteria in the format: columnFilters=attributeName,keyword,value&colu")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edge_nodes_for_distribution_zone(ctx, id, globalFilter, columnFilters, page, size, sort, cmd_fmt, cmd_query):
    """Get all Virtual Edge Nodes for a Distribution Zone"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v2/distribution-zones/{id}/virtual-edge-nodes"
    params = {}
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if columnFilters is not None:
        params["columnFilters"] = columnFilters
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

@group.command("get-loggers-for-all-virtual-edges")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_loggers_for_all_virtual_edges(ctx, cmd_fmt, cmd_query):
    """Get loggers for all virtual edges"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edges/loggers"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-virtual-edge-node-firewall-rules")
@click.argument("id")
@click.option("--deviceGroup", "deviceGroup", type=str, default=None, help="Device Group name")
@click.option("--policyGroup", "policyGroup", type=str, required=True, help="Policy Group name")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter — searches across ruleName, ruleSource, application, sourceZone, s")
@click.option("--columnFilters", "columnFilters", type=str, default=None, help="Column-specific filter in the format: columnFilters=attributeName,keyword,value.")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_virtual_edge_node_firewall_rules(ctx, id, deviceGroup, policyGroup, globalFilter, columnFilters, page, size, sort, cmd_fmt, cmd_query):
    """List of Firewalls and Firewall rules for given Virtual Edge Node with pagination"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/firewall-rules"
    params = {}
    if deviceGroup is not None:
        params["deviceGroup"] = deviceGroup
    if policyGroup is not None:
        params["policyGroup"] = policyGroup
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if columnFilters is not None:
        params["columnFilters"] = columnFilters
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

@group.command("get-ve-ns-overview-response")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_ve_ns_overview_response(ctx, cmd_fmt, cmd_query):
    """Returns a non-paginated overview, having name and status, of Virtual Edge Nodes."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-nodes-overview"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("is-imbalanced")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_is_imbalanced(ctx, id, cmd_fmt, cmd_query):
    """Check if Virtual Edge Group is imbalanced"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/virtual-edge-groups/{id}/is-imbalanced"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-target-site-history")
@click.argument("type_param")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_target_site_history(ctx, type_param, cmd_fmt, cmd_query):
    """Retrieves the full history for a specific target type."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/targets/{type_param}/history"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-target-types")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_target_types(ctx, cmd_fmt, cmd_query):
    """Get all available target types"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/targets/types"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-site-count")
@click.option("--durationInHours", "durationInHours", type=int, required=True, help="Site created within last these many hours.")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_site_count(ctx, durationInHours, cmd_fmt, cmd_query):
    """Get site count"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/sites/count"
    params = {}
    if durationInHours is not None:
        params["durationInHours"] = durationInHours
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-all-ve-ns-for-global-credentials")
@click.argument("credentialsid")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter — searches across ip, hostname, and siteId")
@click.option("--columnFilters", "columnFilters", type=str, default=None, help="Column-specific filter in the format: columnFilters=attributeName,keyword,value.")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_ve_ns_for_global_credentials(ctx, credentialsid, globalFilter, columnFilters, sort, page, size, cmd_fmt, cmd_query):
    """Get Virtual Edge Nodes using a global credential"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/global-credentials/{credentialsid}/virtual-edge-nodes"
    params = {}
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if columnFilters is not None:
        params["columnFilters"] = columnFilters
    if sort is not None:
        params["sort"] = sort
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

@group.command("get-distribution-zone")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_distribution_zone(ctx, id, cmd_fmt, cmd_query):
    """Get single Distribution Zone"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/distribution-zones/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("delete-distribution-zone")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_distribution_zone(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete Distribution Zone"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/distribution-zones/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-dashboard-count")
@click.option("--siteIds", "siteIds", type=str, default=None, help="List of site identifiers to filter by")
@click.option("--type", "type_param", type=str, default=None, help="Type of Virtual Edge (VE) group to filter by")
@click.option("--durationInHours", "durationInHours", type=int, required=True, help="Time window in hours for counting newly created VEs and VENs")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_dashboard_count(ctx, siteIds, type_param, durationInHours, cmd_fmt, cmd_query):
    """Get VE and VEN dashboard count"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/topology/v1/dashboard/count"
    params = {}
    if siteIds is not None:
        params["siteIds"] = siteIds
    if type_param is not None:
        params["type"] = type_param
    if durationInHours is not None:
        params["durationInHours"] = durationInHours
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("force-delete-ven")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_force_delete_ven(ctx, id, cmd_fmt, cmd_query, confirm):
    """Force delete a Virtual Edge Node in decommission state"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/virtual-edge-nodes/{id}/force"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("bulk-delete-credentials")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_bulk_delete_credentials(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Bulk delete global credentials"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/global-credentials/bulk/delete"
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
        result = client.delete(endpoint, params=params, data=body)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("bulk-delete-cloud-controllers")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_bulk_delete_cloud_controllers(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Bulk delete Mist cloud controllers"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/topology/v1/cloud-controller/bulk/delete"
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
        result = client.delete(endpoint, params=params, data=body)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)
