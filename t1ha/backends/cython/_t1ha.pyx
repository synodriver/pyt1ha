# cython: language_level=3
# cython: cdivision=True
import cython

from cpython.mem cimport PyMem_Free, PyMem_Malloc
from libc.stdint cimport uint8_t, uint64_t

from t1ha.backends.cython cimport t1ha


cpdef inline uint64_t hash(const uint8_t[::1] data, uint64_t seed):
    cdef uint64_t ret
    with nogil:
        ret = t1ha.t1ha0(<void*>&data[0], <size_t>data.shape[0], seed)
    return ret

cpdef inline tuple hash128(const uint8_t[::1] data, uint64_t seed):
    cdef  uint64_t extra_data, ret  # high 64, low 64
    with nogil:
        ret = t1ha.t1ha2_atonce128(&extra_data,<void*>&data[0], <size_t> data.shape[0], seed)
    return extra_data, ret

@cython.final
@cython.no_gc
@cython.freelist(8)
cdef class Hash:
    cdef t1ha.t1ha_context_t  ctx

    def __cinit__(self, uint64_t seed_x,  uint64_t seed_y):
        with nogil:
            t1ha.t1ha2_init(&self.ctx, seed_x, seed_y)

    cpdef inline update(self, const uint8_t[::1] data):
        with nogil:
            t1ha.t1ha2_update(&self.ctx, <void *>&data[0], <size_t>data.shape[0])

    cpdef inline tuple final(self):
        cdef uint64_t extra_data, ret  # high 64, low 64
        with nogil:
            ret = t1ha.t1ha2_final(&self.ctx,&extra_data)
        return extra_data, ret
