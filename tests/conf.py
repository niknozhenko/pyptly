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
    api = pyptly.Aptly("http://127.0.0.1:8080")
    repo_name = 'aptly-repo'
    repo_comment = 'New test repository'
    repo_component = 'main'
    repo_distr = 'test_distr'
    upload_dir = 'python-packages'
    test_pkg1 = 'tests/files/python-talloc_2.1.2-0+deb8u1_amd64.deb'
    test_pkg21 = 'tests/files/python-gdbm_2.7.8-2+b1_amd64.deb'
