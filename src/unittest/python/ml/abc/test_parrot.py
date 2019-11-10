from unittest import TestCase
import unittest

from ml.abc import Parrot


class TestParrot(TestCase):
    def test_fly(self):
        self.assertRaises(TypeError, Parrot)

if __name__ == '__main__':
    unittest.main()
