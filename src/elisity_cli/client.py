"""
Unified CCC API client with OAuth2 auth, retry, pagination, and NDJSON support.
"""

import json
import logging
import time
from typing import Any, Dict, Iterator, List, Optional
from urllib.parse import urljoin

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)


class CCCClient:
    """HTTP client for the Elisity Cloud Control Center API."""

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        timeout: int = 30,
        verify_ssl: bool = True,
    ):
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self.access_token: Optional[str] = None
        self.token_expiry: float = 0
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def authenticate(self) -> bool:
        """Obtain OAuth2 token via client_credentials grant."""
        token_url = (
            f"{self.base_url}/auth/realms/elisity/protocol/openid-connect/token"
        )
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "openid",
        }
        try:
            resp = requests.post(
                token_url,
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=self.timeout,
                verify=self.session.verify,
            )
            resp.raise_for_status()
            data = resp.json()
            self.access_token = data["access_token"]
            # Refresh 60s before actual expiry
            self.token_expiry = time.time() + data.get("expires_in", 300) - 60
            self.session.headers["Authorization"] = f"Bearer {self.access_token}"
            logger.debug("OAuth2 authentication successful")
            return True
        except requests.exceptions.HTTPError as e:
            logger.error("Auth failed: HTTP %s — %s", e.response.status_code, e.response.text[:200])
            return False
        except Exception as e:
            logger.error("Auth failed: %s", e)
            return False

    def _ensure_auth(self):
        if not self.access_token or time.time() >= self.token_expiry:
            if not self.authenticate():
                raise RuntimeError("CCC authentication failed. Check credentials.")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(
            (requests.exceptions.ConnectionError, requests.exceptions.Timeout)
        ),
        reraise=True,
    )
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Any = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> requests.Response:
        self._ensure_auth()
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        merged_headers = {}
        if headers:
            merged_headers.update(headers)
        resp = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            timeout=self.timeout,
            headers=merged_headers,
        )
        # On 401 retry auth once
        if resp.status_code == 401:
            logger.debug("Got 401, refreshing token...")
            self.access_token = None
            self._ensure_auth()
            resp = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout,
                headers=merged_headers,
            )
        return resp

    def request_raw(
        self,
        method: str,
        endpoint: str,
        data: Any = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> requests.Response:
        """Make a raw request and return the Response object."""
        resp = self._request(method, endpoint, data=data, params=params, headers=headers)
        resp.raise_for_status()
        return resp

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        resp = self._request("GET", endpoint, params=params)
        resp.raise_for_status()
        if not resp.text or not resp.text.strip():
            return {}
        try:
            return resp.json()
        except ValueError:
            # Some CCC endpoints return text/plain or empty-ish 200 bodies
            # (e.g. /api/flows/v1/noisedefinition when nothing is defined).
            # Surface the raw text rather than crashing the parser.
            logger.warning("Non-JSON 200 from %s; returning raw text", endpoint)
            return {"raw": resp.text}

    def get_ndjson(self, endpoint: str, params: Optional[Dict] = None) -> List[dict]:
        """GET for endpoints that may return NDJSON."""
        self._ensure_auth()
        url = urljoin(self.base_url + "/", endpoint.lstrip("/"))
        resp = self.session.get(
            url, params=params, headers={"Accept": "*/*"}, timeout=self.timeout
        )
        resp.raise_for_status()
        if not resp.text:
            return []
        ct = resp.headers.get("content-type", "")
        if "ndjson" in ct:
            return [json.loads(line) for line in resp.text.strip().split("\n") if line.strip()]
        try:
            data = resp.json()
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                return data.get("content", data.get("items", [data]))
            return [data]
        except ValueError:
            return [json.loads(line) for line in resp.text.strip().split("\n") if line.strip()]

    def post(self, endpoint: str, data: Any = None, params: Optional[Dict] = None) -> Any:
        resp = self._request("POST", endpoint, data=data, params=params)
        resp.raise_for_status()
        if not resp.text:
            return {}
        try:
            return resp.json()
        except ValueError:
            return resp.text.strip().strip('"')

    def put(self, endpoint: str, data: Any = None, params: Optional[Dict] = None) -> Any:
        resp = self._request("PUT", endpoint, data=data, params=params)
        resp.raise_for_status()
        if not resp.text:
            return {}
        try:
            return resp.json()
        except ValueError:
            return resp.text.strip()

    def patch(self, endpoint: str, data: Any = None, params: Optional[Dict] = None) -> Any:
        resp = self._request("PATCH", endpoint, data=data, params=params)
        resp.raise_for_status()
        if not resp.text:
            return {}
        return resp.json()

    def delete(self, endpoint: str, params: Optional[Dict] = None, data: Any = None) -> Any:
        resp = self._request("DELETE", endpoint, data=data, params=params)
        resp.raise_for_status()
        if not resp.text:
            return {}
        try:
            return resp.json()
        except ValueError:
            return {}

    def paginate(
        self, endpoint: str, params: Optional[Dict] = None, page_size: int = 100
    ) -> Iterator[dict]:
        """Auto-paginate a Spring Boot paginated endpoint."""
        params = dict(params or {})
        params["size"] = page_size
        page = 0
        while True:
            params["page"] = page
            result = self.get(endpoint, params=params)
            if isinstance(result, dict) and "content" in result:
                items = result["content"]
                yield from items
                if result.get("last", True):
                    break
                page += 1
            elif isinstance(result, list):
                yield from result
                break
            else:
                yield result
                break

    def health_check(self) -> Dict:
        """Quick health check against the sites endpoint."""
        try:
            self._ensure_auth()
            resp = self._request("GET", "/api/topology/v2/sites", params={"size": 1})
            return {"status": "healthy", "code": resp.status_code, "authenticated": True}
        except Exception as e:
            return {"status": "error", "error": str(e), "authenticated": False}
