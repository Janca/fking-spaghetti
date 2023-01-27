from fking.network.proxies import load_proxies, mark_bad_proxy, next_proxy

# noinspection PyUnresolvedReferences
__all__ = [
    # proxies
    "load_proxies",
    "mark_bad_proxy",
    "next_proxy",

    # module properties
    "default_headers"
]

default_headers: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.3"
}
