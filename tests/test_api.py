import pyptly
import six
from nose.tools import assert_is_instance
from .conf import AptlyTestCase


class Test_api(AptlyTestCase):

    def test_aptly_version(self):
        version = self.api.aptly_version()
        assert_is_instance(version, dict)
        assert_is_instance(version['Version'], six.string_types)


    def test_aptly_version(self):
        repos = self.api.get_local_repos()
        assert_is_instance(repos, list)
