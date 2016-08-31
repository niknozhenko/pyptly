import pyptly
import six

if six.PY3:
    import unittest
else:
    import unittest2 as unittest


class AptlyTestCase(unittest.TestCase):
    def setUp(self):
        self.api = pyptly.Aptly("http://127.0.0.1:8080")
