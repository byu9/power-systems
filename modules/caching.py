"""
Caching Wrappers
"""

__all__ = [
    'lru_cache',
    'cached_property',
    'Disk_Cache',
]


try:
    from functools import lru_cache

except ImportError:
    from backports.functools_lru_cache import lru_cache


try:
    from functools import cached_property

except ImportError:
    from backports.cached_property import cached_property


from diskcache import Cache as Disk_Cache
