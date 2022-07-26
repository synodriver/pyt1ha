"""
Copyright (c) 2008-2022 synodriver <synodriver@gmail.com>
"""
import os
import platform

impl = platform.python_implementation()


def _should_use_cffi() -> bool:
    ev = os.getenv("T1HA_USE_CFFI")
    if ev is not None:
        return True
    if impl == "CPython":
        return False
    else:
        return True


if not _should_use_cffi():
    from t1ha.backends.cython import Hash, hash, hash128
else:
    from t1ha.backends.cffi import Hash, hash, hash128
