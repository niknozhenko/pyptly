import pyptly
import os
import six
from .conf import (AptlyTestCase, assert_is_instance, assert_equals,
                   assert_in, assert_true)


class Test_local_repo_methods(AptlyTestCase):

    def test_get_local_repos(self):
        repos = self.api.get_local_repos()
        assert_is_instance(repos, list)

    def test_1_create_local_repo(self):
        new_repo = self.api.create_local_repo(
                                        self.repo_name,
                                        Comment=self.repo_comment,
                                        DefaultDistribution=self.repo_distr,
                                        DefaultComponent=self.repo_component)
        assert_equals(new_repo['Name'], self.repo_name)
        assert_equals(new_repo['Comment'], self.repo_comment)
        assert_equals(new_repo['DefaultDistribution'], self.repo_distr)
        assert_equals(new_repo['DefaultComponent'], self.repo_component)

    def test_2_show_local_repo(self):
        repo_info = self.api.show_local_repo(self.repo_name)
        assert_equals(repo_info['Name'], self.repo_name)
        assert_equals(repo_info['Comment'], self.repo_comment)
        assert_equals(repo_info['DefaultDistribution'], self.repo_distr)
        assert_equals(repo_info['DefaultComponent'], self.repo_component)

    def test_3_edit_local_repo(self):
        new_comment = 'changed comment'
        new_dist = 'new_distr'
        new_component = 'mainnew'
        edited_repo = self.api.edit_local_repo(
                                        self.repo_name,
                                        Comment=new_comment,
                                        DefaultDistribution=new_dist,
                                        DefaultComponent=new_component)
        assert_equals(edited_repo['Comment'], new_comment)
        assert_equals(edited_repo['DefaultDistribution'], new_dist)
        assert_equals(edited_repo['DefaultComponent'], new_component)

    def test_4_delete_local_repo(self):
        del_repo = self.api.delete_local_repo(self.repo_name)
        assert_true(not bool(del_repo))


class Test_misc_methods(AptlyTestCase):

    def test_aptly_version(self):
        version = self.api.aptly_version()
        assert_is_instance(version, dict)
        assert_is_instance(version['Version'], six.string_types)


    def test_get_graph(self):
        file_path = self.api.get_graph()
        assert os.path.exists(file_path['Path'])


class Test_package_api(AptlyTestCase):

    @classmethod
    def setUpClass(cls):
        cls.api.create_local_repo(cls.repo_name)
        cls.api.upload_files(cls.upload_dir,
                             [cls.test_pkg1, cls.test_pkg2, cls.test_pkg3])

    @classmethod
    def tearDownClass(cls):
        cls.api.delete_local_repo(cls.repo_name)

    def test_1_add_uploaded_pkg(self):
        added_pkg = self.api.add_uploaded_pkg(
                                    self.repo_name, self.upload_dir,
                                    filename=os.path.basename(self.test_pkg1))
        assert_true(not bool(added_pkg['FailedFiles']))
        added_pkgs = self.api.add_uploaded_pkg(self.repo_name, self.upload_dir)
        assert_true(not bool(added_pkgs['FailedFiles']))


    def test_2_show_repo_packages(self):
        repo_pkgs = self.api.show_repo_packages(self.repo_name)
        assert_true(bool(repo_pkgs))


    def test_2_show_pkg_bykey(self):
        repo_pkgs = self.api.show_repo_packages(self.repo_name)
        escaped_key = repo_pkgs[0].replace(' ', '%20')
        pkg = self.api.show_pkg_bykey(escaped_key)
        assert_in('ShortKey', pkg)


    def test_3_delete_pkg_bykey(self):
        repo_pkgs = self.api.show_repo_packages(self.repo_name)
        repo_info = self.api.show_local_repo(self.repo_name) 
        del_pkg = self.api.delete_pkg_bykey(self.repo_name,
                                            PackageRefs=[repo_pkgs[0]])
        assert_equals(repo_info, del_pkg)


class Test_snapshots(AptlyTestCase):

    @classmethod
    def setUpClass(cls):
        cls.api.create_local_repo(cls.repo_name)
        cls.api.upload_files(cls.upload_dir,
                             [cls.test_pkg1, cls.test_pkg2, cls.test_pkg3])

    @classmethod
    def tearDownClass(cls):
        cls.api.delete_local_repo(cls.repo_name)

    def test_1_create_snapshot_from_repo(self):
        snaps = self.api.create_snapshot_from_repo(self.repo_name,
                                                   Name='snap_test')
        assert_in('Name', snaps)
        assert_in('CreatedAt', snaps)


class Test_upload_files(AptlyTestCase):

    @classmethod
    def setUpClass(cls):
        cls.api.create_local_repo(cls.repo_name)

    @classmethod
    def tearDownClass(cls):
        cls.api.delete_local_repo(cls.repo_name)

    def test_1_get_dirs(self):
        dirs = self.api.get_dirs()
        assert_is_instance(dirs, list)

    def test_2_upload_files(self):
        upload_test1 = self.api.upload_files(self.upload_dir, self.test_pkg1)
        assert_equals(upload_test1[0],
                      self.upload_dir + '/' + os.path.basename(self.test_pkg1))

        upload_test2 = self.api.upload_files(self.upload_dir, [self.test_pkg2,
                                                               self.test_pkg3])

        for pkg in [self.test_pkg2, self.test_pkg3]:
            assert_in(self.upload_dir + '/' + os.path.basename(pkg),
                      upload_test2)

    def test_3_get_files(self):
        files = self.api.get_files(self.upload_dir)
        for pkg in [self.test_pkg1, self.test_pkg2, self.test_pkg3]:
            assert_in(os.path.basename(pkg), files)

    def test_4_delete_file(self):
        rm_file = self.api.delete_file(self.upload_dir,
                                       os.path.basename(self.test_pkg1))
        assert_true(not bool(rm_file))


    def test_5_delete_dir(self):
        rm_dir = self.api.delete_dir(self.upload_dir)
        assert_true(not bool(rm_dir))

