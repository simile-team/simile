# simile/api_requestor.py
import requests
from . import config
from .error import AuthenticationError, RequestError, ApiKeyNotSetError

def request(method, endpoint, params=None, data=None, json=None, headers=None, timeout=30):
    # Refer back to config.api_key so changes to config are seen here
    if not config.api_key:
        raise ApiKeyNotSetError("No API key set. Please set simile.api_key = '...'")

    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint

    url = config.api_base.rstrip("/") + endpoint

    # Common default headers
    default_headers = {
        "Authorization": f"Api-Key {config.api_key}",
        "Content-Type": "application/json",
    }
    if headers:
        default_headers.update(headers)

    try:
        resp = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=default_headers,
            timeout=timeout
        )
    except requests.exceptions.RequestException as e:
        raise RequestError(f"Request error: {e}")

    # Check for typical authentication or 4xx/5xx issues
    if resp.status_code == 401:
        raise AuthenticationError("Invalid or missing API key.")
    elif 400 <= resp.status_code < 600:
        # For all other error codes, raise a generic error
        raise RequestError(
            f"Error from server (status {resp.status_code}): {resp.text}",
            status_code=resp.status_code,
            response=resp.text
        )

    return resp
