"""
Copyright (c) 2008-2022 synodriver <synodriver@gmail.com>
"""
import glob

from cffi import FFI

ffibuilder = FFI()
ffibuilder.cdef(
    """
// typedef struct {
// uint64_t a;
// uint64_t b;
// uint64_t c;
// uint64_t d;
// } _tmp; 
    
typedef union {
 ...;    // fuck
} t1ha_state256_t;

typedef struct t1ha_context {
  ...;
} t1ha_context_t;

uint64_t t1ha0( void *data, size_t length, uint64_t seed);

uint64_t t1ha2_atonce128(uint64_t *extra_result,
                                  void *data, size_t length,
                                  uint64_t seed);
                                  
void t1ha2_init(t1ha_context_t *ctx, uint64_t seed_x, uint64_t seed_y);
void t1ha2_update(t1ha_context_t *ctx, const void *data, size_t length);
uint64_t t1ha2_final(t1ha_context_t *ctx, uint64_t *extra_result);
    """
)

source = """
#include <stdint.h>
#include "t1ha.h"
"""

ffibuilder.set_source(
    "t1ha.backends.cffi._t1ha",
    source,
    sources=glob.glob("./dep/src/*.c"),
    include_dirs=["./dep"],
)

if __name__ == "__main__":
    ffibuilder.compile()
