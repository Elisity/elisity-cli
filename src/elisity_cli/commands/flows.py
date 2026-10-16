"""
Traffic analytics — device state, flow search, noise definitions

Auto-generated from the Elisity CCC OpenAPI specification.
"""

import click

from elisity_cli.context import CliContext, pass_context
from elisity_cli.output import render


@click.group("flows")
@pass_context
def group(ctx):
    """Traffic analytics — device state, flow search, noise definitions"""
    pass

@group.command("get-raw-traffic-summary")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_raw_traffic_summary(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Get traffic summary data"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/nflowsearch/api/v1/trafficsummary"
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

@group.command("get-traffic-record")
@click.option("--offset", "offset", type=int, required=True, help="offset")
@click.option("--size", "size", type=int, required=True, help="size")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_traffic_record(ctx, offset, size, body_data, body_file, cmd_fmt, cmd_query):
    """POST /nflowsearch/api/v1/trafficRecord"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/nflowsearch/api/v1/trafficRecord"
    params = {}
    if offset is not None:
        params["offset"] = offset
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

@group.command("traffic-record-export")
@click.option("--offset", "offset", type=int, required=True, help="offset")
@click.option("--size", "size", type=int, required=True, help="size")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_traffic_record_export(ctx, offset, size, body_data, body_file, cmd_fmt, cmd_query):
    """Export traffic records as CSV"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/nflowsearch/api/v1/trafficRecord/export"
    params = {}
    if offset is not None:
        params["offset"] = offset
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

@group.command("get-pg-data")
@click.option("--format-param", "format", type=str, required=True, help="[sends format] format")
@click.option("--size", "size", type=int, required=True, help="size")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_pg_data(ctx, format, size, body_data, body_file, cmd_fmt, cmd_query):
    """POST /nflowsearch/api/v1/pgdata"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/nflowsearch/api/v1/pgdata"
    params = {}
    if format is not None:
        params["format"] = format
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

@group.command("flows-export")
@click.option("--size", "size", type=int, default=20, help="Number of results to return")
@click.option("--offset", "offset", type=int, required=True, help="offset")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_flows_export(ctx, size, offset, body_data, body_file, cmd_fmt, cmd_query):
    """Generate flows export as CSV"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/nflowsearch/api/v1/flowdata"
    params = {}
    if size is not None:
        params["size"] = size
    if offset is not None:
        params["offset"] = offset
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

@group.command("get-distribution-zone-sankey")
@click.option("--offset", "offset", type=int, default=0, help="Offset for the result set")
@click.option("--size", "size", type=int, default=20, help="Number of results to return")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_distribution_zone_sankey(ctx, offset, size, body_data, body_file, cmd_fmt, cmd_query):
    """Get distribution zone sankey data"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/nflowsearch/api/v1/distributionzone"
    params = {}
    if offset is not None:
        params["offset"] = offset
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

@group.command("get-dash-board-summary-data")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_dash_board_summary_data(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """POST /nflowsearch/api/v1/dashboardSummary"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/nflowsearch/api/v1/dashboardSummary"
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

@group.command("get-noise-definition")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_noise_definition(ctx, cmd_fmt, cmd_query):
    """GET /api/flows/v1/noisedefinition"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/flows/v1/noisedefinition"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-noise-definition")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_noise_definition(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """POST /api/flows/v1/noisedefinition"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/flows/v1/noisedefinition"
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

@group.command("get-unique-values")
@click.option("--parameter", "parameter", type=str, required=True, help="parameter")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_unique_values(ctx, parameter, cmd_fmt, cmd_query):
    """Get unique values"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/nflowsearch/api/v1/unique-values"
    params = {}
    if parameter is not None:
        params["parameter"] = parameter
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-exclusion-filter-candidates")
@click.option("--search", "search", type=str, default=None, help="Search text to filter by name, port, or protocol")
@click.option("--page", "page", type=int, default=0, help="Page number (0-based)")
@click.option("--size", "size", type=int, default=100, help="Page size (1-1000)")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_exclusion_filter_candidates(ctx, search, page, size, cmd_fmt, cmd_query):
    """Get exclusion filter candidate port+protocol pairs ranked by traffic usage"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/nflowsearch/api/v1/port-information/exclusion-filter-candidates"
    params = {}
    if search is not None:
        params["search"] = search
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

@group.command("get-heatmap")
@click.argument("deviceid")
@click.option("--month", "month", type=str, required=True, help="month")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_heatmap(ctx, deviceid, month, cmd_fmt, cmd_query):
    """GET /nflowsearch/api/v1/devices/{deviceId}/heatmap"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/nflowsearch/api/v1/devices/{deviceid}/heatmap"
    params = {}
    if month is not None:
        params["month"] = month
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-capabilities")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_capabilities(ctx, cmd_fmt, cmd_query):
    """Get analytics capabilities"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/nflowsearch/api/v1/capabilities"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-available-ports")
@click.option("--search", "search", type=str, default=None, help="Search text to filter by name, port, or protocol")
@click.option("--page", "page", type=int, default=0, help="Page number (0-based)")
@click.option("--size", "size", type=int, default=100, help="Page size")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_available_ports(ctx, search, page, size, cmd_fmt, cmd_query):
    """Get all available ports and their names"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/flows/v1/port-information/ports"
    params = {}
    if search is not None:
        params["search"] = search
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

@group.command("search-noise-definitions")
@click.option("--query-param", "query", type=str, default=None, help="[sends query] query")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_search_noise_definitions(ctx, query, cmd_fmt, cmd_query):
    """GET /api/flows/v1/noisedefinition/search"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/flows/v1/noisedefinition/search"
    params = {}
    if query is not None:
        params["query"] = query
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)
