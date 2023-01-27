import os
import time
from typing import Optional as _Optional, Union as _Union

_proxy_timeout = 120_000
_proxy_path = os.path.abspath("./proxies.txt")

_proxies: dict[str, float] = {}
_proxies_timeout: dict[str, float] = {}


def load_proxies(path: _Optional[str] = None) -> list[str]:
    global _proxies, _proxy_path

    if path:
        _proxy_path = path

    if os.path.isfile(_proxy_path):
        with open(_proxy_path, 'r') as f:
            proxies = f.read().splitlines()
            _proxies.clear()

            for proxy in proxies:
                key = proxy.strip()
                if key and key not in _proxies:
                    _proxies[key] = -1

    return list(_proxies.keys())


def next_proxy() -> _Optional[dict[str, str]]:
    global _proxies

    if len(_proxies) <= 0:
        return None

    best_timeout: float = -1
    best_proxy: _Optional[str] = None

    time_now = time.time()
    for proxy, timeout in _proxies.items():
        if proxy in _proxies_timeout:
            bad_timeout = _proxies_timeout[proxy]
            diff = time_now - bad_timeout
            if diff >= _proxy_timeout:
                del _proxies_timeout[proxy]
            else:
                continue

        if best_proxy is None:
            best_proxy = proxy
            best_timeout = timeout
        elif best_timeout > timeout:
            best_proxy = proxy
            best_timeout = timeout

    if best_proxy is None:
        return None

    _proxies[best_proxy] = time.time()

    return {
        'http': best_proxy,
        'https': best_proxy
    }


def mark_bad_proxy(proxy: _Optional[_Union[dict[str, str], str]]):
    global _proxies_timeout

    if proxy is None:
        return

    if not isinstance(proxy, str):
        proxy = proxy["http"]

    _proxies_timeout[proxy] = time.time()
