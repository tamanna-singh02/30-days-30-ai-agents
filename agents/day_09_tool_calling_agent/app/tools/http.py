from urllib.parse import urlparse

import requests


ALLOWED_HOSTS = {
    "jsonplaceholder.typicode.com",
    "api.github.com",
}


def http_get(url: str) -> str:

    try:

        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            return "Blocked: unsupported URL scheme."

        if parsed.hostname not in ALLOWED_HOSTS:
            return (
                f"Blocked: host '{parsed.hostname}' "
                "is not allowed."
            )

        response = requests.get(
            url,
            timeout=10,
        )

        response.raise_for_status()

        return response.text[:5000]

    except requests.RequestException as e:

        return f"HTTP request error: {str(e)}"