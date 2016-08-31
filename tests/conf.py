import pyptly
import six
from nose.tools import assert_equals, assert_true


# assert_is_instance appeared in python 3.2 and was backported to 2.7
try:
    from nose.tools import assert_is_instance
except ImportError:
    def assert_is_instance(obj, cls, msg=None):
        assert_true(isinstance(obj, cls), msg)


if six.PY3:
    import unittest
else:
    import unittest2 as unittest


class AptlyTestCase(unittest.TestCase):
    def setUp(self):
        self.api = pyptly.Aptly("http://127.0.0.1:8080")
        self.repo_name = 'aptly-repo'
        self.repo_comment = 'New test repository'
        self.repo_component = 'main'
        self.repo_distr = 'test_distr'
