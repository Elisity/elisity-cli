"""
Device identity and enrichment — CRUD, bulk, attach, enrich, events

Auto-generated from the Elisity CCC OpenAPI specification.
"""

import click

from elisity_cli.context import CliContext, pass_context
from elisity_cli.output import render


@click.group("devices")
@pass_context
def group(ctx):
    """Device identity and enrichment — CRUD, bulk, attach, enrich, events"""
    pass

@group.command("get-all-settings")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_settings(ctx, cmd_fmt, cmd_query):
    """Get all offline purge settings grouped by configuration"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/purge-settings"
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
    """Update offline purge settings (global and policy groups)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/purge-settings"
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

@group.command("get-custom-oui-mappings")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_custom_oui_mappings(ctx, cmd_fmt, cmd_query):
    """Get custom OUI mappings"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/data/oui"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("apply-custom-oui-mappings")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_apply_custom_oui_mappings(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Upload custom OUI mappings and override existing ones"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/data/oui"
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

@group.command("get-configuration-by-id")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_configuration_by_id(ctx, id, cmd_fmt, cmd_query):
    """Get time-based configuration by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/time-based-access-configuration/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-configuration")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_configuration(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update time-based configuration"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/time-based-access-configuration/{id}"
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

@group.command("delete-configuration")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_configuration(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete time-based configuration"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/identity-graph/v1/time-based-access-configuration/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update suppression entry"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/suppression/{id}"
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

@group.command("delete")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete suppression entry"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/identity-graph/v1/suppression/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-device")
@click.argument("id")
@click.option("--target-enrichment-layer", "target_enrichment_layer", type=str, default=None, help="target-enrichment-layer")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_device(ctx, id, target_enrichment_layer, body_data, body_file, cmd_fmt, cmd_query):
    """Partially update device by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/{id}"
    params = {}
    if target_enrichment_layer is not None:
        params["target-enrichment-layer"] = target_enrichment_layer
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

@group.command("delete-device")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_device(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete device"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/identity-graph/v1/devices/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("recalculate-attributes")
@click.option("--force-device-state-refresh", "force_device_state_refresh", type=bool, default=False, help="If false, attributes will be recalculated, but Policy Service will be notified o")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_recalculate_attributes(ctx, force_device_state_refresh, cmd_fmt, cmd_query):
    """Recalculate attributes on all devices"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/recalculate-attributes"
    params = {}
    if force_device_state_refresh is not None:
        params["force-device-state-refresh"] = force_device_state_refresh
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("bulk-update-devices")
@click.option("--target-enrichment-layer", "target_enrichment_layer", type=str, default=None, help="target-enrichment-layer")
@click.option("--parallel", "parallel", type=bool, default=True, help="parallel")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_bulk_update_devices(ctx, target_enrichment_layer, parallel, body_data, body_file, cmd_fmt, cmd_query):
    """Update devices by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/bulk"
    params = {}
    if target_enrichment_layer is not None:
        params["target-enrichment-layer"] = target_enrichment_layer
    if parallel is not None:
        params["parallel"] = parallel
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

@group.command("bulk-create-devices")
@click.option("--target-enrichment-layer", "target_enrichment_layer", type=str, default=None, help="target-enrichment-layer")
@click.option("--parallel", "parallel", type=bool, default=True, help="If true, devices will be created in parallel. IMPORTANT: Using this option disab")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_bulk_create_devices(ctx, target_enrichment_layer, parallel, body_data, body_file, cmd_fmt, cmd_query):
    """Create new devices"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/bulk"
    params = {}
    if target_enrichment_layer is not None:
        params["target-enrichment-layer"] = target_enrichment_layer
    if parallel is not None:
        params["parallel"] = parallel
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

@group.command("bulk-delete-devices")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_bulk_delete_devices(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Delete device"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/identity-graph/v1/devices/bulk"
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

@group.command("bulk-recalculate-effective-attributes")
@click.option("--parallel", "parallel", type=bool, default=True, help="If true, effective attributes will be recalculated in parallel. IMPORTANT: Using")
@click.option("--force-device-state-refresh", "force_device_state_refresh", type=bool, default=True, help="If false, effective attributes will be recalculated, but Policy Service won't be")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_bulk_recalculate_effective_attributes(ctx, parallel, force_device_state_refresh, body_data, body_file, cmd_fmt, cmd_query):
    """Recalculate effective attributes by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/bulk/recalculate-effective"
    params = {}
    if parallel is not None:
        params["parallel"] = parallel
    if force_device_state_refresh is not None:
        params["force-device-state-refresh"] = force_device_state_refresh
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

@group.command("get-values-for-device-attribute")
@click.argument("attributename")
@click.option("--source", "source", type=str, default=None, help="source")
@click.option("--queryString", "queryString", type=str, default=None, help="queryString")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_values_for_device_attribute(ctx, attributename, source, queryString, cmd_fmt, cmd_query):
    """Get values for device attribute"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/attributes/{attributename}"
    params = {}
    if source is not None:
        params["source"] = source
    if queryString is not None:
        params["queryString"] = queryString
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("add-device-unique-attribute-value")
@click.argument("attributename")
@click.option("--value", "value", type=str, required=True, help="value")
@click.option("--source", "source", type=str, default=None, help="source")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_add_device_unique_attribute_value(ctx, attributename, value, source, cmd_fmt, cmd_query):
    """Add device attribute unique value"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/attributes/{attributename}"
    params = {}
    if value is not None:
        params["value"] = value
    if source is not None:
        params["source"] = source
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("create-workload")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_workload(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create a static workload"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads"
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

@group.command("get-workloads-view")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_workloads_view(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """List workloads"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/view"
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

@group.command("validate-permissions-existing")
@click.argument("connectorid")
@click.argument("endpointid")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_permissions_existing(ctx, connectorid, endpointid, body_data, body_file, cmd_fmt, cmd_query):
    """Validate AWS permissions for an existing connector endpoint"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/{connectorid}/{endpointid}/validate-permissions"
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

@group.command("list-available-regions-existing")
@click.argument("connectorid")
@click.argument("endpointid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_available_regions_existing(ctx, connectorid, endpointid, cmd_fmt, cmd_query):
    """List available AWS regions for an existing connector endpoint"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/{connectorid}/{endpointid}/regions"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("validate-permissions-pre-creation")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_permissions_pre_creation(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Validate AWS permissions for a new endpoint (pre-creation)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/validate-permissions"
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

@group.command("generate-trust-policy")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_generate_trust_policy(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Generate trust policy JSON for the customer's IAM role"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/setup/aws/trust-policy"
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

@group.command("generate-external-id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_generate_external_id(ctx, cmd_fmt, cmd_query):
    """Generate external ID and account ID for IAM role setup"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/setup/aws/generate-external-id"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("list-available-regions")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_available_regions(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """List available AWS regions for an endpoint's credentials"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/regions"
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

@group.command("discover-ec2workloads")
@click.argument("connectorid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_discover_ec2workloads(ctx, connectorid, cmd_fmt, cmd_query):
    """Discover EC2 workloads for an existing connector"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/ec2/{connectorid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("validate-azure-region-permissions-existing")
@click.argument("connectorid")
@click.argument("endpointid")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_azure_region_permissions_existing(ctx, connectorid, endpointid, body_data, body_file, cmd_fmt, cmd_query):
    """Validate an existing endpoint's region filter against its subscriptions"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/{connectorid}/{endpointid}/validate-region-permissions"
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

@group.command("validate-azure-permissions-existing")
@click.argument("connectorid")
@click.argument("endpointid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_azure_permissions_existing(ctx, connectorid, endpointid, cmd_fmt, cmd_query):
    """Validate Azure permissions for an existing connector endpoint"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/{connectorid}/{endpointid}/validate-permissions"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("validate-azure-connection-existing")
@click.argument("connectorid")
@click.argument("endpointid")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_azure_connection_existing(ctx, connectorid, endpointid, body_data, body_file, cmd_fmt, cmd_query):
    """Validate the Azure connection of an existing endpoint, optionally with edited credentials"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/{connectorid}/{endpointid}/validate-connection"
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

@group.command("list-azure-subscriptions-existing")
@click.argument("connectorid")
@click.argument("endpointid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_azure_subscriptions_existing(ctx, connectorid, endpointid, cmd_fmt, cmd_query):
    """List Azure subscriptions for an existing connector endpoint"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/{connectorid}/{endpointid}/subscriptions"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("preview-azure-scope-existing")
@click.argument("connectorid")
@click.argument("endpointid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_preview_azure_scope_existing(ctx, connectorid, endpointid, cmd_fmt, cmd_query):
    """Preview the scope of an existing endpoint (post-creation scope edit)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/{connectorid}/{endpointid}/scope-preview"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("list-azure-resource-groups-existing")
@click.argument("connectorid")
@click.argument("endpointid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_azure_resource_groups_existing(ctx, connectorid, endpointid, cmd_fmt, cmd_query):
    """List Azure resource groups (with VM counts) for an existing endpoint"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/{connectorid}/{endpointid}/resource-groups"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("list-azure-regions-existing")
@click.argument("connectorid")
@click.argument("endpointid")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_azure_regions_existing(ctx, connectorid, endpointid, body_data, body_file, cmd_fmt, cmd_query):
    """List Azure regions available to an existing endpoint's subscriptions"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/{connectorid}/{endpointid}/regions"
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

@group.command("validate-azure-region-permissions-pre-creation")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_azure_region_permissions_pre_creation(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Validate a new endpoint's region filter against its subscriptions (pre-creation)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/validate-region-permissions"
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

@group.command("validate-azure-permissions-pre-creation")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_azure_permissions_pre_creation(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Validate Azure permissions for a new endpoint (pre-creation)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/validate-permissions"
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

@group.command("validate-azure-connection-pre-creation")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_validate_azure_connection_pre_creation(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Validate Azure connection for a new endpoint (pre-creation)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/validate-connection"
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

@group.command("list-azure-subscriptions-pre-creation")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_azure_subscriptions_pre_creation(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """List Azure subscriptions for a new endpoint (pre-creation)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/subscriptions"
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

@group.command("preview-azure-scope-pre-creation")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_preview_azure_scope_pre_creation(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Preview a scope before creating the connector"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/scope-preview"
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

@group.command("list-azure-resource-groups-pre-creation")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_azure_resource_groups_pre_creation(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """List Azure resource groups (with VM counts) for a new endpoint's scope"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/resource-groups"
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

@group.command("list-azure-regions-pre-creation")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_azure_regions_pre_creation(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """List Azure regions available to a new endpoint's subscriptions (pre-creation)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/regions"
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

@group.command("sync-endpoint")
@click.argument("connectorid")
@click.argument("endpointid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_sync_endpoint(ctx, connectorid, endpointid, cmd_fmt, cmd_query):
    """Trigger immediate workload sync for a specific endpoint"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/connectors/{connectorid}/{endpointid}/sync"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("sync-connector")
@click.argument("connectorid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_sync_connector(ctx, connectorid, cmd_fmt, cmd_query):
    """Trigger immediate workload sync for all endpoints of a connector"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/connectors/{connectorid}/sync"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-workload-aggregate")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_workload_aggregate(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Get workload aggregated counts"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/aggregate"
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

@group.command("get-devices-view")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_devices_view(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Get devices view"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/view"
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

@group.command("refresh-devices-view")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_refresh_devices_view(ctx, cmd_fmt, cmd_query):
    """Refresh DevicesView"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/view/refresh"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("check")
@click.option("--recentChangeThreshold", "recentChangeThreshold", type=str, default=None, help="ISO-8601 duration of the freshness window; devices modified within now − this du")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_check(ctx, recentChangeThreshold, cmd_fmt, cmd_query):
    """Check ig-view-service sync state against the identity-graph DB (no dispatch)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/sync"
    params = {}
    if recentChangeThreshold is not None:
        params["recentChangeThreshold"] = recentChangeThreshold
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("sync")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_sync(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Synchronize ig-view-service from identity-graph by republishing out-of-sync devices"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/sync"
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

@group.command("export-devices")
@click.option("--format-param", "format", type=str, default=None, help="[sends format] Export file format (CSV or XLSX). CSV is deprecated since 26.4.0 ")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export_devices(ctx, format, body_data, body_file, cmd_fmt, cmd_query):
    """Generate devices export"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/export"
    params = {}
    if format is not None:
        params["format"] = format
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

@group.command("get-device-aggregate")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_device_aggregate(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Get devices aggregated count"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/aggregate"
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

@group.command("attach-workloads")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_attach_workloads(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Attach a batch of workloads reported by a VEN"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/workloads/attached"
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

@group.command("attach-workload")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_attach_workload(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Attach a workload reported by a VEN, creating it if it does not exist"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/workloads/attach"
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

@group.command("get-configurations")
@click.option("--status", "status", type=str, default=None, help="Filter configurations by status (CURRENT, UPCOMING, PAST)")
@click.option("--name", "name", type=str, default=None, help="Filter configurations by name pattern (optional)")
@click.option("--ids", "ids", type=str, default=None, help="Filter configurations by specific IDs (comma-separated)")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_configurations(ctx, status, name, ids, cmd_fmt, cmd_query):
    """Get time-based configurations"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/time-based-access-configuration"
    params = {}
    if status is not None:
        params["status"] = status
    if name is not None:
        params["name"] = name
    if ids is not None:
        params["ids"] = ids
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("create-configuration")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_configuration(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create new time-based configuration"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/time-based-access-configuration"
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

@group.command("duplicate-configuration")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_duplicate_configuration(ctx, id, cmd_fmt, cmd_query):
    """Duplicate time-based configuration"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/time-based-access-configuration/{id}/duplicate"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-configurations-by-ids")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_configurations_by_ids(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Get multiple time-based configurations by IDs"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/time-based-access-configuration/query"
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

@group.command("search-suppression-list")
@click.option("--filters", "filters", type=str, required=True, help="filters")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size (max: 1000)")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_search_suppression_list(ctx, filters, page, size, sort, cmd_fmt, cmd_query):
    """Get all entries (paged, searchable and filterable)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/suppression"
    params = {}
    if filters is not None:
        params["filters"] = filters
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

@group.command("create")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create a new suppression entry"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/suppression"
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

@group.command("export-suppression-list")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export_suppression_list(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Export entries as CSV"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/suppression/export"
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

@group.command("get-blended-enrichment-order")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_blended_enrichment_order(ctx, cmd_fmt, cmd_query):
    """Read enrichment order"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/settings/elisity-enrichment-order"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("upsert-enrichment-order")
@click.option("--recalculate-effective-attributes", "recalculate_effective_attributes", type=bool, default=True, help="If true, effective attributes will be recalculated.")
@click.option("--force-device-state-refresh", "force_device_state_refresh", type=bool, default=True, help="If false, effective attributes will be recalculated, but Policy Service won't be")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_upsert_enrichment_order(ctx, recalculate_effective_attributes, force_device_state_refresh, body_data, body_file, cmd_fmt, cmd_query):
    """Update/create settings entry"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/settings/elisity-enrichment-order"
    params = {}
    if recalculate_effective_attributes is not None:
        params["recalculate-effective-attributes"] = recalculate_effective_attributes
    if force_device_state_refresh is not None:
        params["force-device-state-refresh"] = force_device_state_refresh
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

@group.command("delete-enrichment-order")
@click.option("--recalculate-effective-attributes", "recalculate_effective_attributes", type=bool, default=True, help="If true, effective attributes will be recalculated.")
@click.option("--force-device-state-refresh", "force_device_state_refresh", type=bool, default=True, help="If false, effective attributes will be recalculated, but Policy Service won't be")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_enrichment_order(ctx, recalculate_effective_attributes, force_device_state_refresh, cmd_fmt, cmd_query, confirm):
    """Delete enrichment order settings entry"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/identity-graph/v1/settings/elisity-enrichment-order"
    params = {}
    if recalculate_effective_attributes is not None:
        params["recalculate-effective-attributes"] = recalculate_effective_attributes
    if force_device_state_refresh is not None:
        params["force-device-state-refresh"] = force_device_state_refresh
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("feature-flag-ig")
@click.argument("name")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_feature_flag_ig(ctx, name, cmd_fmt, cmd_query):
    """Get current status of a feature flag"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/feature-flag/{name}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("set-feature-flag-ig")
@click.argument("name")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_set_feature_flag_ig(ctx, name, body_data, body_file, cmd_fmt, cmd_query):
    """Set value of a feature flag"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/feature-flag/{name}"
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

@group.command("create-device")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_device(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create a new device"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices"
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

@group.command("enrich-by-id")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_enrich_by_id(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Enrich device by ID."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/{id}/enrich"
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

@group.command("enrich-by-id-append")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_enrich_by_id_append(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Enrich device by ID and append to existing data in layer (create layer if not exists)."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/{id}/enrich"
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

@group.command("execute-synchronous-on-demand-enrichment")
@click.argument("id")
@click.argument("source")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_execute_synchronous_on_demand_enrichment(ctx, id, source, cmd_fmt, cmd_query):
    """Execute a synchronous on demand enrichment of given device with a given source"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/{id}/enrich/{source}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("execute-synchronous-on-demand-enrichment-post")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_execute_synchronous_on_demand_enrichment_post(ctx, id, cmd_fmt, cmd_query):
    """Execute a synchronous on demand enrichment of given device for all sources"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/{id}/enrich-all"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("detach")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_detach(ctx, id, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Detach device by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/identity-graph/v1/devices/{id}/detach"
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

@group.command("enrich-by-ip")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_enrich_by_ip(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Enrich device by IP."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/enrich"
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

@group.command("enrich-by-ip-append")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_enrich_by_ip_append(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Enrich device by IP and append to existing data in layer (create layer if not exists)."""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/enrich"
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

@group.command("detach-by-mac")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_detach_by_mac(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Detach device by MAC and IP"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/identity-graph/v1/devices/detach"
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

@group.command("bulk-create-devices-from-file")
@click.option("--target-enrichment-layer", "target_enrichment_layer", type=str, default=None, help="target-enrichment-layer")
@click.option("--parallel", "parallel", type=bool, default=True, help="parallel")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_bulk_create_devices_from_file(ctx, target_enrichment_layer, parallel, body_data, body_file, cmd_fmt, cmd_query):
    """Create new devices from XLSX file"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/bulk/upload"
    params = {}
    if target_enrichment_layer is not None:
        params["target-enrichment-layer"] = target_enrichment_layer
    if parallel is not None:
        params["parallel"] = parallel
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

@group.command("execute-bulk-refresh")
@click.option("--deviceIds", "deviceIds", type=str, default=None, help="List of device IDs (UUID)")
@click.option("--sources", "sources", type=str, default=None, help="List of sources to enrich")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_execute_bulk_refresh(ctx, deviceIds, sources, body_data, body_file, cmd_fmt, cmd_query):
    """Execute a asynchronous on-demand enrichment of given devices for given sources (bulk)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/bulk/refresh"
    params = {}
    if deviceIds is not None:
        params["deviceIds"] = deviceIds
    if sources is not None:
        params["sources"] = sources
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

@group.command("attached")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_attached(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Attach devices by MAC or create new ones if not exists"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/attached"
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

@group.command("attach")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_attach(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Attach device by MAC or create new one if not exists"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/attach"
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

@group.command("update-workload-interface")
@click.argument("workloadid")
@click.argument("interfaceid")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_workload_interface(ctx, workloadid, interfaceid, body_data, body_file, cmd_fmt, cmd_query):
    """Update STATIC layer of a workload interface"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/{workloadid}/interfaces/{interfaceid}"
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

@group.command("get-workload-details")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_workload_details(ctx, id, cmd_fmt, cmd_query):
    """Get workload by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-workload")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_workload(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update workload STATIC attributes"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/{id}"
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

@group.command("get-specification")
@click.option("--visible", "visible", type=bool, default=False, help="visible")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_specification(ctx, visible, cmd_fmt, cmd_query):
    """Read workload attribute specification"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/specification"
    params = {}
    if visible is not None:
        params["visible"] = visible
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-permissions-policy")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_permissions_policy(ctx, cmd_fmt, cmd_query):
    """Get the IAM permissions policy for ElisityCloudDiscoveryPolicy"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/setup/aws/permissions-policy"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-auth-methods")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_auth_methods(ctx, cmd_fmt, cmd_query):
    """List available AWS authentication methods"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/setup/aws/auth-methods"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("list-azure-required-permissions")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_azure_required_permissions(ctx, cmd_fmt, cmd_query):
    """List the ARM permissions the connector needs, by tier"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/discovery/azure/setup/permissions"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-workload-count")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_workload_count(ctx, cmd_fmt, cmd_query):
    """Get workload count"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/workloads/count"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("search-device")
@click.option("--mac", "mac", type=str, required=True, help="MAC of the device")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_search_device(ctx, mac, cmd_fmt, cmd_query):
    """Search device by MAC"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices"
    params = {}
    if mac is not None:
        params["mac"] = mac
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("read-device")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_read_device(ctx, id, cmd_fmt, cmd_query):
    """Get device by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-device-header-data")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_device_header_data(ctx, cmd_fmt, cmd_query):
    """Get devices count"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/count"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-device-attribute-values")
@click.argument("attributename")
@click.option("--source", "source", type=str, default=None, help="source")
@click.option("--queryString", "queryString", type=str, default=None, help="queryString")
@click.option("--page", "page", type=int, default=None, help="Page number")
@click.option("--size", "size", type=int, default=None, help="Page size (max: 1000)")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column, can only sort by name")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_device_attribute_values(ctx, attributename, source, queryString, page, size, sort, cmd_fmt, cmd_query):
    """Get device attribute values"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/attributes/{attributename}"
    params = {}
    if source is not None:
        params["source"] = source
    if queryString is not None:
        params["queryString"] = queryString
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

@group.command("get-device-attribute-values-with-display-names")
@click.argument("attributename")
@click.option("--queryString", "queryString", type=str, default=None, help="queryString")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_device_attribute_values_with_display_names(ctx, attributename, queryString, cmd_fmt, cmd_query):
    """Get values with displayNames for an attribute"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/devices/attributes/{attributename}/values"
    params = {}
    if queryString is not None:
        params["queryString"] = queryString
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("read-all-layer-instances-specification")
@click.option("--visible", "visible", type=bool, default=False, help="visible")
@click.option("--includeWorkloads", "includeWorkloads", type=bool, default=True, help="includeWorkloads")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_read_all_layer_instances_specification(ctx, visible, includeWorkloads, cmd_fmt, cmd_query):
    """Read dynamic specification of all layers"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/data/specification"
    params = {}
    if visible is not None:
        params["visible"] = visible
    if includeWorkloads is not None:
        params["includeWorkloads"] = includeWorkloads
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("read-static-layer-specification")
@click.argument("source")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_read_static_layer_specification(ctx, source, cmd_fmt, cmd_query):
    """Read static layer specification"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/data/specification/static/{source}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("list-all-custom-connector-icons-base64")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_all_custom_connector_icons_base64(ctx, cmd_fmt, cmd_query):
    """List all Custom Connector icons (base64)"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v2/data/specification/icons"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("search-by-name")
@click.option("--name", "name", type=str, required=True, help="name")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_search_by_name(ctx, name, cmd_fmt, cmd_query):
    """Search time-based configurations by name"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/time-based-access-configuration/search"
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

@group.command("get-raw-enrichment-order")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_raw_enrichment_order(ctx, cmd_fmt, cmd_query):
    """Read raw enrichment order settings entry"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/settings/elisity-enrichment-order/raw"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-enrichment-order-dto")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_enrichment_order_dto(ctx, cmd_fmt, cmd_query):
    """Read enrichment order settings entry"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/settings/elisity-enrichment-order/dto"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("read-all-settings")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_read_all_settings(ctx, cmd_fmt, cmd_query):
    """Read all settings entries"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/settings/all"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("read-history-for-device")
@click.argument("id")
@click.option("--time_from", "time_from", type=str, default=None, help="ISO-8601 timestamp to search from (inclusive). Epoch if empty.")
@click.option("--time_to", "time_to", type=str, default=None, help="ISO-8601 timestamp to search to (inclusive). Now if empty.")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_read_history_for_device(ctx, id, time_from, time_to, cmd_fmt, cmd_query):
    """Read device event history by device ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/{id}/events"
    params = {}
    if time_from is not None:
        params["time_from"] = time_from
    if time_to is not None:
        params["time_to"] = time_to
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-device-header-data-get")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_device_header_data_get(ctx, cmd_fmt, cmd_query):
    """Get devices count"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/count"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("check-ven-availability")
@click.argument("nodeid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_check_ven_availability(ctx, nodeid, cmd_fmt, cmd_query):
    """Check if VEN is able to accept device attach"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph/v1/devices/attach/can-accept-from/{nodeid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("purge-device-layer")
@click.argument("id")
@click.argument("source")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_purge_device_layer(ctx, id, source, cmd_fmt, cmd_query, confirm):
    """Purge device layer"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/identity-graph/v1/devices/{id}/{source}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("bulk-purge-device-layers")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_bulk_purge_device_layers(ctx, body_data, body_file, cmd_fmt, cmd_query, confirm):
    """Bulk purge device layers"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/identity-graph/v1/devices/bulk/purge"
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

@group.command("devices-view")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_devices_view(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Query devices with CSearch filters"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph-view/v2/devices/view"
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

@group.command("export-devices-from-view")
@click.option("--format-param", "format", type=str, default=None, help="[sends format] Export file format (CSV or XLSX). CSV is deprecated since 26.4.0 ")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_export_devices_from_view(ctx, format, body_data, body_file, cmd_fmt, cmd_query):
    """Export devices to CSV or XLSX"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph-view/v2/devices/export"
    params = {}
    if format is not None:
        params["format"] = format
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

@group.command("devices-aggregate")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_devices_aggregate(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Get device aggregate counts"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph-view/v2/devices/aggregate"
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

@group.command("stream-digest")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_stream_digest(ctx, cmd_fmt, cmd_query):
    """Stream device digest"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph-view/v2/devices/digest"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get_ndjson(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("devices-count")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_devices_count(ctx, cmd_fmt, cmd_query):
    """Get device counts"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/identity-graph-view/v2/devices/count"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)
