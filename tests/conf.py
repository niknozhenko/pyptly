import pyptly
import six
from nose.tools import assert_equals, assert_true, assert_raises


# assert_is_instance appeared in python 3.2 and was backported to 2.7
try:
    from nose.tools import assert_is_instance
except ImportError:
    def assert_is_instance(obj, cls, msg=None):
        assert_true(isinstance(obj, cls), msg)


# assert_not_in and assert_less appeared in python 3.1 and was backported to 2.7
try:
    from nose.tools import (assert_not_in, assert_less, assert_less_equal,
                            assert_in, assert_greater)
except ImportError:
    def assert_not_in(member, collection, msg=None):
        assert_true(member not in collection, msg)

    def assert_less(a, b, msg=None):
        assert_true(a < b, msg)

    def assert_less_equal(a, b, msg=None):
        assert_true(a <= b, msg)

    def assert_in(member, collection, msg=None):
        assert_true(member in collection, msg)

    def assert_greater(a, b, msg=None):
        assert_true(a > b, msg)


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
    test_pkg2 = 'tests/files/python-gdbm_2.7.8-2+b1_amd64.deb'
    test_pkg3 = 'tests/files/unzip_6.0-16+deb8u2_amd64.deb'
    snapshot_name1 = 'snap-test1'
    snapshot_name2 = 'snap-test2'
    snapshot_description = 'test description'
    publish_distr = 'jessie'
    prefix = '.'
