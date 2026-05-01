import requests

DEFAULT_TIMEOUT = 10


def post_json(url, payload, headers=None, timeout=DEFAULT_TIMEOUT):
    return requests.post(url, json=payload, headers=headers, timeout=timeout)


def get_json(url, headers=None, timeout=DEFAULT_TIMEOUT):
    return requests.get(url, headers=headers, timeout=timeout)

__all__ = ['post_json', 'get_json']
