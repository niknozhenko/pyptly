import pyptly
import six
from nose.tools import assert_is_instance

def test_aptly_version():
    aptly = pyptly.Aptly("http://127.0.0.1:8080")
    version = aptly.aptly_version()
    assert_is_instance(version, dict)
    assert_is_instance(version['Version'], six.string_types)


def test_aptly_version():
    aptly = pyptly.Aptly("http://127.0.0.1:8080")
    repos = aptly.get_local_repos()
    assert_is_instance(repos, list)
