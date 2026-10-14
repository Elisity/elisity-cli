"""
Device updates that cannot knock a device offline (ENG-31142).

`PUT /api/identity-graph/v1/devices/{id}` is a full replace: a body without
`ip` (absent, null or "") is read by CCC as "remove the static IP" and detaches
the device — `DeviceDetachedEvent reason="Static removal of IP address"`, device
Offline. A label-only update is exactly that body. `ipAddress` is not a request
field, so sending it changes nothing.

CCC 26.10 adds `PATCH` on the same path, where an omitted ip/venId keeps the
current value. CCC 26.9 and earlier answer that PATCH with 405. So
`update-device`:

1. GETs the device and fills each of `ip`, `mac`, `venId` the body leaves unset
   with the device's current value — the workaround CCC's own label handlers use
   (ccc b25ab765667). Safe on every version, and it makes the PUT fallback safe.
2. Sends the filled body with PATCH; on 405 resends the same body with PUT.

`--allow-ip-removal` skips both and sends the body as given with PUT, the only
way to deliberately remove a static IP.

This module is hand-written and lives outside `commands/` so that
`generate_commands.py` never overwrites it. The generator emits the call to
`update_device()` and the `--allow-ip-removal` flag for the operations in its
KEEP_DEVICE_ATTACHMENT_OPERATIONS.
"""

from typing import Any, Dict, List, Optional

import click
import requests

from elisity_cli.client import CCCClient

# v2 returns top-level ip/mac/venId (verified live). The OpenAPI DeviceDetailsDto
# does not document them, so this path is pinned here rather than derived.
DEVICE_READ_PATH = "/api/identity-graph/v2/devices/{id}"

ATTACHMENT_FIELDS = ("ip", "mac", "venId")

# What CCC 26.9 and earlier answer to PATCH on the device path.
PATCH_NOT_SUPPORTED = 405


def _is_unset(value: Any) -> bool:
    # CCC reads null and "" the same as an absent ip: removal.
    return value is None or value == ""


def read_device(client: CCCClient, device_id: str) -> Dict[str, Any]:
    """Read the device, or raise. Never returns a device we cannot trust."""
    try:
        device = client.get(DEVICE_READ_PATH.format(id=device_id))
    except Exception as e:
        raise RuntimeError(
            f"could not read device {device_id} to keep its ip/mac/venId ({e}); "
            "nothing was sent"
        ) from e
    # client.get() turns an empty 200 into {} and a non-JSON 200 into {"raw": ...}.
    if not isinstance(device, dict) or not device or set(device) == {"raw"}:
        raise RuntimeError(
            f"device {device_id} read returned no usable device record; nothing was sent"
        )
    return device


def fill_attachment(body: Dict[str, Any], device: Dict[str, Any]) -> List[str]:
    """Fill unset ip/mac/venId from the device, in place. Returns the filled names.

    A device with no current IP has no attachment to lose: the body is left
    exactly as given.
    """
    if _is_unset(device.get("ip")):
        return []
    filled = []
    for field in ATTACHMENT_FIELDS:
        if _is_unset(body.get(field)) and not _is_unset(device.get(field)):
            body[field] = device[field]
            filled.append(field)
    return filled


def _decode(resp: requests.Response) -> Any:
    # Same decoding as CCCClient.put(), which the PUT path has always used.
    if not resp.text:
        return {}
    try:
        return resp.json()
    except ValueError:
        return resp.text.strip()


def update_device(
    client: CCCClient,
    endpoint: str,
    device_id: str,
    body: Any,
    params: Optional[Dict] = None,
    allow_ip_removal: bool = False,
) -> Any:
    """Update a device without detaching it. See the module docstring."""
    if allow_ip_removal:
        return client.put(endpoint, data=body, params=params)

    if not isinstance(body, dict):
        # Nothing to fill into, and a PUT fallback would carry no ip.
        raise ValueError(
            "update-device needs a JSON object body (--body or --body-file); nothing was sent"
        )

    body = dict(body)
    filled = fill_attachment(body, read_device(client, device_id))

    used_put = False
    try:
        result = _decode(client.request_raw("PATCH", endpoint, data=body, params=params))
    except requests.exceptions.HTTPError as e:
        if e.response is None or e.response.status_code != PATCH_NOT_SUPPORTED:
            raise
        # CCC 26.9 and earlier: no PATCH on this path. The body already carries
        # the device's current ip, so the full-replace PUT keeps it attached.
        used_put = True
        try:
            result = client.put(endpoint, data=body, params=params)
        except Exception as put_error:
            raise RuntimeError(
                f"PATCH is not supported by this CCC (405); the PUT fallback failed: {put_error}"
            ) from put_error

    if filled or used_put:
        parts = []
        if filled:
            parts.append(f"kept the device's current {', '.join(filled)} in the update")
        if used_put:
            parts.append("sent the update with PUT because this CCC does not support PATCH (26.9 or earlier)")
        click.echo(
            f"Note: {'; '.join(parts)}. Use --allow-ip-removal to send the body as given with PUT.",
            err=True,
        )
    return result
