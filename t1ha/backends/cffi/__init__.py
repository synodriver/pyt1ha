"""
Copyright (c) 2008-2022 synodriver <synodriver@gmail.com>
"""
from typing import Tuple

from t1ha.backends.cffi._t1ha import ffi, lib


def hash(data: bytes, seed: int) -> int:
    return lib.t1ha0(ffi.cast("void*", ffi.from_buffer(data)), len(data), seed)


def hash128(data: bytes, seed: int) -> tuple:
    # cdef  uint64_t extra_data, ret  # high 64, low 64
    extra_data = ffi.new("uint64_t*")
    ret = lib.t1ha2_atonce128(
        extra_data, ffi.cast("void*", ffi.from_buffer(data)), len(data), seed
    )
    return extra_data[0], ret


class Hash:
    # cdef t1ha.t1ha_context_t  ctx

    def __init__(self, seed_x: int, seed_y: int):
        self.ctx = ffi.new("t1ha_context_t*")
        lib.t1ha2_init(self.ctx, seed_x, seed_y)

    def update(self, data: bytes):
        lib.t1ha2_update(self.ctx, ffi.cast("void*", ffi.from_buffer(data)), len(data))

    def final(self) -> Tuple[int]:
        # cdef uint64_t extra_data, ret  # high 64, low 64
        extra_data = ffi.new("uint64_t*")
        ret = lib.t1ha2_final(self.ctx, extra_data)
        return extra_data[0], ret
