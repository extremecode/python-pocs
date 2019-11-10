from unittest import TestCase
import unittest

from ml.abc import Falcon
from ml.abc import Bird


class TestParrot(TestCase):
    def test_instance(self):
        f = Falcon()
        self.assertTrue(isinstance(f,Bird))
        self.assertTrue(isinstance(f,Falcon))
        self.assertEqual("flying",f.fly())
        
if __name__ == '__main__':
    unittest.main()