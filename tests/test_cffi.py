"""
Copyright (c) 2008-2022 synodriver <synodriver@gmail.com>
"""
import os

os.environ["T1HA_USE_CFFI"] = "1"

from unittest import TestCase
from random import randint

from t1ha import hash, hash128, Hash


class TestAll(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_hash(self):
        for i in range(1000):
            seed = randint(0, 1000)
            self.assertEqual(hash(b"12", seed), hash(b"12", seed))

    def test_hash_128(self):
        for i in range(1000):
            seed = randint(0, 1000)
            self.assertEqual(hash128(b"12", seed), hash128(b"12", seed))

    def test_hash_stream(self):
        for i in range(1000):
            seed_x = randint(0, 1000)
            seed_y = randint(0, 1000)
            hasher = Hash(seed_x, seed_y)
            hasher.update(b"1hfsaohfspao")
            d1 = hasher.final()

            hasher2 = Hash(seed_x, seed_y)
            hasher2.update(b"1hfsaohfspao")
            d2 = hasher2.final()
            self.assertEqual(d1, d2)


if __name__ == "__main__":
    import unittest

    unittest.main()
