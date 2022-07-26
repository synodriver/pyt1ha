# cython: language_level=3
# cython: cdivision=True
from libc.stdint cimport uint8_t, uint32_t, uint64_t


cdef extern from 't1ha.h' nogil:
    ctypedef struct _tmp:
        uint64_t a
        uint64_t b
        uint64_t c
        uint64_t d

    ctypedef union t1ha_state256_t:
        uint8_t bytes[32]
        uint32_t u32[8]
        uint64_t u64[4]
        _tmp n

    ctypedef struct t1ha_context_t:
        t1ha_state256_t state
        t1ha_state256_t buffer
        size_t partial
        uint64_t total

    bint t1ha_selfcheck__t1ha0_ia32aes_noavx()
    bint t1ha_selfcheck__t1ha0_ia32aes_avx()
    bint t1ha_selfcheck__t1ha0_ia32aes_avx2()

    uint64_t t1ha2_atonce(const void *data, size_t length, uint64_t seed)
    uint64_t t1ha2_atonce128(uint64_t *extra_result,   # output high 64bit
                                  void *data, size_t length,
                                  uint64_t seed)

    void t1ha2_init(t1ha_context_t *ctx, uint64_t seed_x, uint64_t seed_y)
    void t1ha2_update(t1ha_context_t * ctx, void * data, size_t length)
    uint64_t t1ha2_final(t1ha_context_t *, uint64_t * extra_result)

    uint64_t t1ha1_le(const void *data, size_t length, uint64_t seed)
    uint64_t t1ha1_be(const void *data, size_t length, uint64_t seed)

    # The little-endian variant for 32-bit CPU. */
    uint64_t t1ha0_32le(const void *data, size_t length, uint64_t seed)
    # The big-endian variant for 32-bit CPU. */
    uint64_t t1ha0_32be(const void *data, size_t length, uint64_t seed)

    uint64_t t1ha0_ia32aes_noavx(const void *data, size_t length, uint64_t seed)
    uint64_t t1ha0_ia32aes_avx(const void *data, size_t length, uint64_t seed)
    uint64_t t1ha0_ia32aes_avx2(const void *data, size_t length, uint64_t seed)

    ctypedef uint64_t(*t1ha0_function_t)(const void *, size_t, uint64_t)
    t1ha0_function_t t1ha0_resolve()

    uint64_t t1ha0( void *data, size_t length, uint64_t seed)
    uint64_t (*t1ha0_funcptr)(const void *data, size_t length,
                              uint64_t seed)