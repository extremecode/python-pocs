from unittest import TestCase
import unittest

from ml.HelloWorld import hello

class HelloWorldTest(TestCase):
    def test_hello_world_message(self):
        self.assertEqual("hello World",hello())

if __name__ == '__main__':
    unittest.main()
