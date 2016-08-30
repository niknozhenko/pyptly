import pyptly
import six

try:
    from nose.tools import assert_is_instance
except ImportError:
    def assert_is_instance(obj, cls, msg=None):
        assert_true(isinstance(obj, cls), msg)


def test_aptly_version():
    aptly = pyptly.Aptly("http://127.0.0.1:8080")
    version = aptly.aptly_version()
    assert_is_instance(version, dict)
    assert_is_instance(version['Version'], six.string_types)
