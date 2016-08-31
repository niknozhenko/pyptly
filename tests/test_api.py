import pyptly
import six
from nose.tools import assert_equals, assert_is_instance
from .conf import AptlyTestCase


class Test_api(AptlyTestCase):

    def test_aptly_version(self):
        version = self.api.aptly_version()
        assert_is_instance(version, dict)
        assert_is_instance(version['Version'], six.string_types)


    def test_get_local_repos(self):
        repos = self.api.get_local_repos()
        assert_is_instance(repos, list)


    def test_create_local_repo(self):
        new_repo = self.api.create_local_repo(
                                        self.repo_name,
                                        Comment=self.repo_comment,
                                        DefaultDistribution=self.repo_distr,
                                        DefaultComponent=self.repo_component)
        assert_equals(new_repo['Name'], self.repo_name)
        assert_equals(new_repo['Comment'], self.repo_comment)
        assert_equals(new_repo['DefaultDistribution'], self.repo_distr)
        assert_equals(new_repo['DefaultComponent'], self.repo_component)
