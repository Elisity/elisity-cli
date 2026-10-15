"""
System operations — tasks, specs, state sync

Auto-generated from the Elisity CCC OpenAPI specification.
"""

import click

from elisity_cli.context import CliContext, pass_context
from elisity_cli.output import render


@click.group("system")
@pass_context
def group(ctx):
    """System operations — tasks, specs, state sync"""
    pass

@group.command("get-task")
@click.argument("taskid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_task(ctx, taskid, cmd_fmt, cmd_query):
    """Get task by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/{taskid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-task")
@click.argument("taskid")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_task(ctx, taskid, body_data, body_file, cmd_fmt, cmd_query):
    """Update task"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/{taskid}"
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

@group.command("cancel-task")
@click.argument("taskid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_cancel_task(ctx, taskid, cmd_fmt, cmd_query, confirm):
    """Cancel task"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/state-sync/v1/tasks/{taskid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("release-execution-of-task")
@click.argument("taskid")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_release_execution_of_task(ctx, taskid, body_data, body_file, cmd_fmt, cmd_query):
    """Release task"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/{taskid}/release"
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

@group.command("ack-execution-of-task")
@click.argument("taskid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_ack_execution_of_task(ctx, taskid, cmd_fmt, cmd_query):
    """Acknowledge task without result payload"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/{taskid}/ack"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.put(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("ack-execution-of-task-post")
@click.argument("taskid")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_ack_execution_of_task_post(ctx, taskid, body_data, body_file, cmd_fmt, cmd_query):
    """Acknowledge task with result payload"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/{taskid}/ack"
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

@group.command("get-all-configs")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_all_configs(ctx, cmd_fmt, cmd_query):
    """Get all task broker configs"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/config"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("replace-tenant-default")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_replace_tenant_default(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Replace tenant-wide disabled task types"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/config"
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

@group.command("get-effective-config")
@click.argument("veid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_effective_config(ctx, veid, cmd_fmt, cmd_query):
    """Get effective config for a VE"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/config/{veid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("replace-for-ve")
@click.argument("veid")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_replace_for_ve(ctx, veid, body_data, body_file, cmd_fmt, cmd_query):
    """Replace per-VE disabled task types"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/config/{veid}"
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

@group.command("delete-for-ve")
@click.argument("veid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_for_ve(ctx, veid, cmd_fmt, cmd_query, confirm):
    """Remove per-VE override"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/state-sync/v1/tasks/config/{veid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("list-tasks")
@click.option("--globalFilter", "globalFilter", type=str, default=None, help="Global filter")
@click.option("--columnFilter", "columnFilter", type=str, default=None, help="Filtering criteria in the format: columnFilter=attributeName,keyword,value&colum")
@click.option("--page", "page", type=str, default=None, help="Page number")
@click.option("--size", "size", type=str, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_tasks(ctx, globalFilter, columnFilter, page, size, sort, cmd_fmt, cmd_query):
    """List tasks"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks"
    params = {}
    if globalFilter is not None:
        params["globalFilter"] = globalFilter
    if columnFilter is not None:
        params["columnFilter"] = columnFilter
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

@group.command("create-task")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_task(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create a new task"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks"
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

@group.command("list-specs")
@click.option("--page", "page", type=str, default=None, help="Page number")
@click.option("--size", "size", type=str, default=None, help="Page size")
@click.option("--sort", "sort", type=str, default=None, help="Sort by column")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_list_specs(ctx, page, size, sort, cmd_fmt, cmd_query):
    """List all specs"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/specs"
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

@group.command("register-specs")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_register_specs(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Register or update VE specs"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/specs"
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

@group.command("get-spec")
@click.argument("veid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_spec(ctx, veid, cmd_fmt, cmd_query):
    """Get spec by VE ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/specs/{veid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-spec-by-site-id")
@click.argument("siteid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_spec_by_site_id(ctx, siteid, cmd_fmt, cmd_query):
    """Get specs by site ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/specs/site/{siteid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-spec-group-id")
@click.argument("groupid")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_spec_group_id(ctx, groupid, cmd_fmt, cmd_query):
    """Get specs by VE group ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/specs/group/{groupid}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("get-next-task-for-ve")
@click.option("--connectorId", "connectorId", type=str, default=None, help="Optional connector identifier to filter tasks")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_get_next_task_for_ve(ctx, connectorId, cmd_fmt, cmd_query):
    """Poll next task for VE"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/state-sync/v1/tasks/next"
    params = {}
    if connectorId is not None:
        params["connectorId"] = connectorId
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("retrieve-snapshot-schedule")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_retrieve_snapshot_schedule(ctx, id, cmd_fmt, cmd_query):
    """Get snapshot schedule by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/reporting/v1/snapshot-schedules/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("update-snapshot-schedule")
@click.argument("id")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_update_snapshot_schedule(ctx, id, body_data, body_file, cmd_fmt, cmd_query):
    """Update snapshot schedule"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/reporting/v1/snapshot-schedules/{id}"
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

@group.command("delete-snapshot-schedule")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@click.option("--confirm/--no-confirm", default=False, help="Confirm destructive operation")
@pass_context
def cmd_delete_snapshot_schedule(ctx, id, cmd_fmt, cmd_query, confirm):
    """Delete snapshot schedule"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    if not confirm:
        click.echo("Use --confirm to execute this destructive operation.", err=True)
        raise SystemExit(1)
    endpoint = f"/api/reporting/v1/snapshot-schedules/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.delete(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("resume-snapshot-schedule")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_resume_snapshot_schedule(ctx, id, cmd_fmt, cmd_query):
    """Resume snapshot schedule"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/reporting/v1/snapshot-schedules/{id}/resume"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("pause-snapshot-schedule")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_pause_snapshot_schedule(ctx, id, cmd_fmt, cmd_query):
    """Pause snapshot schedule"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/reporting/v1/snapshot-schedules/{id}/pause"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.post(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("search-snapshot-schedules")
@click.option("--name", "name", type=str, default=None, help="Filter by name (partial match, case-insensitive)")
@click.option("--description", "description", type=str, default=None, help="Filter by description (partial match, case-insensitive)")
@click.option("--source", "source", type=str, default=None, help="Filter by report source (exact match)")
@click.option("--status", "status", type=str, default=None, help="Filter by status (exact match)")
@click.option("--type", "type_param", type=str, default=None, help="Filter by type: ONE_TIME or RECURRING")
@click.option("--createdBy", "createdBy", type=str, default=None, help="Filter by created by (partial match, case-insensitive)")
@click.option("--page", "page", type=int, default=0, help="Zero-based page index (0..N)")
@click.option("--size", "size", type=int, default=20, help="The size of the page to be returned")
@click.option("--sort", "sort", type=str, default=['name,ASC'], help="Sorting criteria in the format: property,(asc|desc). Default sort order is ascen")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_search_snapshot_schedules(ctx, name, description, source, status, type_param, createdBy, page, size, sort, cmd_fmt, cmd_query):
    """Search snapshot schedules"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/reporting/v1/snapshot-schedules"
    params = {}
    if name is not None:
        params["name"] = name
    if description is not None:
        params["description"] = description
    if source is not None:
        params["source"] = source
    if status is not None:
        params["status"] = status
    if type_param is not None:
        params["type"] = type_param
    if createdBy is not None:
        params["createdBy"] = createdBy
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

@group.command("create-snapshot-schedule")
@click.option("--body", "body_data", type=str, default=None, help="Request body as JSON string")
@click.option("--body-file", "body_file", type=click.Path(exists=True), default=None, help="Read request body from JSON file")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_create_snapshot_schedule(ctx, body_data, body_file, cmd_fmt, cmd_query):
    """Create snapshot schedule"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/reporting/v1/snapshot-schedules"
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

@group.command("retrieve-snapshot-pdf")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_retrieve_snapshot_pdf(ctx, id, cmd_fmt, cmd_query):
    """Get snapshot PDF"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/reporting/v1/snapshots/{id}.pdf"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("retrieve-snapshot-markdown")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_retrieve_snapshot_markdown(ctx, id, cmd_fmt, cmd_query):
    """Get snapshot Markdown"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/reporting/v1/snapshots/{id}.md"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("retrieve-snapshot-evidence")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_retrieve_snapshot_evidence(ctx, id, cmd_fmt, cmd_query):
    """Get snapshot evidence package"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/reporting/v1/snapshots/{id}.evidence.json"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("retrieve-snapshot")
@click.argument("id")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_retrieve_snapshot(ctx, id, cmd_fmt, cmd_query):
    """Get snapshot by ID"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/reporting/v1/snapshots/{id}"
    params = None
    client = ctx.ensure_client()
    try:
        result = client.get(endpoint, params=params)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    render(result, ctx.format, ctx.query)

@group.command("search-snapshots")
@click.option("--schedule", "schedule", type=str, default=None, help="Filter by schedule ID (exact match)")
@click.option("--scheduleName", "scheduleName", type=str, default=None, help="Filter by schedule name (partial match, case-insensitive)")
@click.option("--scheduleDescription", "scheduleDescription", type=str, default=None, help="Filter by schedule description (partial match, case-insensitive)")
@click.option("--source", "source", type=str, default=None, help="Filter by report source (exact match)")
@click.option("--status", "status", type=str, default=None, help="Filter by status (exact match)")
@click.option("--page", "page", type=int, default=0, help="Zero-based page index (0..N)")
@click.option("--size", "size", type=int, default=20, help="The size of the page to be returned")
@click.option("--sort", "sort", type=str, default=['createdAt,DESC'], help="Sorting criteria in the format: property,(asc|desc). Default sort order is ascen")
@click.option("--format", "-f", "cmd_fmt", type=click.Choice(["json", "table", "yaml", "csv"]), default=None, help="Output format override", hidden=True)
@click.option("--query", "-q", "cmd_query", type=str, default=None, help="JMESPath query override", hidden=True)
@pass_context
def cmd_search_snapshots(ctx, schedule, scheduleName, scheduleDescription, source, status, page, size, sort, cmd_fmt, cmd_query):
    """Search snapshots"""
    if cmd_fmt:
        ctx.format = cmd_fmt
    if cmd_query:
        ctx.query = cmd_query
    endpoint = f"/api/reporting/v1/snapshots"
    params = {}
    if schedule is not None:
        params["schedule"] = schedule
    if scheduleName is not None:
        params["scheduleName"] = scheduleName
    if scheduleDescription is not None:
        params["scheduleDescription"] = scheduleDescription
    if source is not None:
        params["source"] = source
    if status is not None:
        params["status"] = status
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
