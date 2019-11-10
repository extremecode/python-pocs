from unittest import TestCase
import unittest

from ml.abc import Robin
from ml.abc import Bird


class TestParrot(TestCase):
    def test_instance(self):
        r = Robin()
        self.assertTrue(isinstance(r,Bird))
        self.assertTrue(isinstance(r,Robin))

if __name__ == '__main__':
    unittest.main()