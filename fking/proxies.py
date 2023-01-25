import os
import time
from typing import Optional, Union

_proxy_timeout = 120_000
_proxy_path = os.path.abspath("./proxies.txt")
_proxies_timeouts: dict[str, float] = {}
_proxies_bad_timeouts: dict[str, float] = {}


def load_proxies():
    global _proxies_timeouts
    if os.path.isfile(_proxy_path):
        with open(_proxy_path, 'r') as f:
            proxies = f.read().splitlines()
            _proxies: dict[str, int] = {}

            for proxy in proxies:
                key = proxy.strip()
                if key and key not in _proxies:
                    _proxies[key] = -1

            _proxies_timeouts = _proxies

    print(f"Loaded {len(_proxies_timeouts)} proxies...")


def next_best_proxy() -> Optional[dict[str, str]]:
    global _proxies_timeouts

    if len(_proxies_timeouts) <= 0:
        return None

    best_timeout: float = -1
    best_proxy: Optional[str] = None

    time_now = time.time()
    for proxy, timeout in _proxies_timeouts.items():
        if proxy in _proxies_bad_timeouts:
            bad_timeout = _proxies_bad_timeouts[proxy]
            diff = time_now - bad_timeout
            if diff >= _proxy_timeout:
                del _proxies_bad_timeouts[proxy]
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

    _proxies_timeouts[best_proxy] = time.time()

    return {
        'http': best_proxy,
        'https': best_proxy
    }


def mark_bad_proxy(proxy: Optional[Union[dict[str, str], str]]):
    global _proxies_bad_timeouts

    if proxy is None:
        return

    if not isinstance(proxy, str):
        mark_bad_proxy(proxy['http'])
    else:
        _proxies_bad_timeouts[proxy] = time.time()
