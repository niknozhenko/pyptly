import base64
import json
import requests
from pyptly.utils import prefix_sanitized, response

class Aptly(object):
    """Aptly class"""

    def __init__(self, host, user=None, password=None, verify_ssl=True):
        self.headers = {}
        if user and password:
            self.headers['Authorization'] = 'Basic ' + base64.b64encode(
                                                user + ':' + password)
        if not host:
            raise ValueError('host argument may not be empty')
        self.host = host.rstrip('/')
        if self.host.startswith('http://') or self.host.startswith('https://'):
            pass
        else:
            self.host = 'https://' + self.host

        self.api = self.host + "/api"
        self.api_url = {'repos': self.api + '/repos',
                        'snapshots': self.api + '/snapshots',
                        'publish': self.api + '/publish',
                        'files': self.api + '/files',
                        'packages': self.api + '/packages'}
        self.verify_ssl = verify_ssl


    def get_local_repos(self):
        """Show list of currently available local repositories.
        Each repository is returned as in "show" API
        """
        request = requests.get("{0}".format(self.api_url['repos']),
                               headers=self.headers, verify=self.verify_ssl)
        return response(request)


    def create_local_repo(self, name, **kwargs):
        """Create empty local repository with specified parameters

        :param name: name of the new local repository
        :param comment: text describing local repository, for the user
        :param distr: default distribution when publishing from this 
        local repo
        :param component: default component when publishing from this
        local repo
        """
        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        data = {'Name': name}
        if kwargs:
            data.update(kwargs)
    
        request = requests.post("{0}".format(self.api_url['repos']),
                                data=json.dumps(data), headers=headers,
                                verify=self.verify_ssl)
        return response(request)


    def show_local_repo(self, name):
        """Returns basic information about local repository
        :param name: name of the new local repository
        """
        request = requests.get("{0}/{1}".format(self.api_url['repos'], name),
                               headers=self.headers, verify=self.verify_ssl)
        return response(request)


    def show_repo_packages(self, name, **kwargs):
        """List all packages in local repository or perform search on
        repository contents and return result
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.get("{0}/{1}/packages".format(
                               self.api_url['repos'], name), params=params, 
                               headers=self.headers, verify=self.verify_ssl)
        return response(request)


    def edit_local_repo(self, name, **kwargs):
        """Update local repository meta information

        :param name: name of the new local repository
        :param comment: text describing local repository, for the user
        :param distr: default distribution when publishing from this
        local repo
        :param component: default component when publishing from this
        local repo
        """
        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        data = {}
        if kwargs:
            data.update(kwargs)

        request = requests.put('{0}/{1}'.format(self.api_url['repos'], name),
                               data=json.dumps(data), headers=headers,
                               verify=self.verify_ssl)
        return response(request)


    def delete_local_repo(self, name, **kwargs):
        """Delete local repository. Local repository can't be deleted
        if it is published. If local repository has snapshots, aptly
        would refuse to delete it by default, but that can be overridden
        with force flag

        :param force: when value is set to True, delete local repository
        even if it has snapshots
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.delete('{0}/{1}'.format(
                                  self.api_url['repos'], name),
                                  headers=self.headers,
                                  verify=self.verify_ssl,
                                  params=params)
        return response(request)


    def add_uploaded_pkg(self, name, dirname, **kwargs):
        """Import packages from files to the local repository. If
        directory specified, aptly would discover package files
        automatically. Adding same package to local repository is
        not an error.
        By default aptly would try to remove every successfully
        processed file and directory :dir (if it becomes empty
        after import).

        :param name: name of the local repository
        :param dirname: directory with uploaded packages to import
        :param file: file to import
        :param no_rm: when value is set to True, don't remove any file
        :param force_repl: when value is set to True, remove packages 
        conflicting with package being added (in local repository)
        """

        filename = kwargs.pop('file', None)
        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.post('{0}/{1}/{2}/{3}'.format(
                                self.api_url['repos'], name, dirname,
                                filename if filename else ''),
                                headers=self.headers, verify=self.verify_ssl,
                                params=params)
        return response(request)


    def add_pkg_bykey(self, name, **kwargs):
        """Add packages to local repository by package keys.

        Any package could be added, it should be part of aptly database
        (it could come from any mirror, snapshot, other local
        repository). This API combined with package list (search) APIs
        allows to implement importing, copying, moving packages around.

        API verifies that packages actually exist in aptly database and 
        checks constraint that conflicting packages can't be part of the
        same local repository.

        :param name: name of the local repository
        :param pkg_ref: list of package references (package keys)
        """
        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        data = {}
        if kwargs:
            data.update(kwargs)

        request = requests.post('{0}/{1}/packages'.format(
                                self.api_url['repos'], name),
                                data=json.dumps(data), headers=headers,
                                verify=self.verify_ssl)
        return response(request)


    def delete_pkg_bykey(self, name, **kwargs):
        """Remove packages from local repository by package keys.

        Any package(s) could be removed from local repository. List
        package references in local repository could be retrieved with
        show_repo_packages

        :param name: name of the local repository
        :param pkg_ref: list of package references (package keys)
        """
        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        data = {}
        if kwargs:
            data.update(kwargs)

        request = requests.delete('{0}/{1}/packages'.format(
                                  self.api_url['repos'], name),
                                  data=json.dumps(data), headers=headers,
                                  verify=self.verify_ssl)
        return response(request)


    def show_pkg_bykey(self, key):
        """Show information about package by package key.
        Package keys could be obtained from various
        GET .../packages APIs.

        :param key: package key
        """
        request = requests.get('{0}/{1}'.format(self.api_url['packages'], 
                               key), headers=self.headers,
                               verify=self.verify_ssl)
        return response(request)


    def get_dirs(self):
        """List all directories"""
        request = requests.get('{0}'.format(self.api_url['files']),
                               headers=self.headers, verify=self.verify_ssl)
        return response(request)


    def get_files(self, dir):
        """Returns list of files in directory

        :param dir: directory name to inspect
        """
        request = requests.get('{0}/{1}'.format(self.api_url['files'], dir),
                               headers=self.headers, verify=self.verify_ssl)
        return response(request)


    def delete_dir(self, dir):
        """Deletes all files in upload directory and directory itself

        :param dir: directory name to delete
        """
        request = requests.delete('{0}/{1}'.format(self.api_url['files'], dir),
                                  headers=self.headers, verify=self.verify_ssl)
        return response(request)


    def delete_file(self, dir, file):
        """Delete single file in directory

        :param dir: directory to delete from
        :param file: file to delete
        """
        request = requests.delete('{0}/{1}/{2}'.format(self.api_url['files'],
                                  dir, file), headers=self.headers,
                                  verify=self.verify_ssl)
        return response(request)


    def upload_files(self, dir, files):
        """Parameter :dir is upload directory name. Directory would be
        created if it doesn't exist.

        Any number of files can be uploaded in one call, aptly would
        preserve filenames. No check is performed if existing uploaded
        would be overwritten.

        :param dir: upload directory name
        :param files: files to upload. Single file path or list of pathes.
        """
        if isinstance(files, list):
            files = [('file', open(f, 'rb')) for f in files]
        else:
            files = ('file', open(files, 'rb'))

        request = requests.post('{0}/{1}'.format(self.api_url['files'], dir),
                                files=files,headers=self.headers,
                                verify=self.verify_ssl)
        return response(request)


    def get_publish(self):
        """List published repositories"""
        request = requests.get('{0}'.format(self.api_url['publish']),
                               headers=self.headers, verify=self.verify_ssl)
        return response(request)


    def publish(self, **kwargs):
        """Publish local repository or snapshot under specified prefix.
        Storage might be passed in prefix as well, e.g. s3:packages/.
        """
        prefix = kwargs.pop('prefix', None)
        if prefix:
            prefix = prefix_sanitized(prefix)

        data = kwargs
        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        request = requests.post('{0}/{1}'.format(self.api_url['publish'],
                                prefix if prefix else ''), headers=headers,
                                data=json.dumps(data), verify=self.verify_ssl)
        return response(request)


    def update_publish(self, distr, **kwargs):
        """API action depends on published repository contents:
        * if local repository has been published, published repository
        would be updated to match local repository contents
        * if snapshots have been been published, it is possible to
        switch each component to new snapshot
        """
        prefix = kwargs.pop('prefix', None)
        if prefix:
            prefix = prefix_sanitized(prefix)

        data = {}
        if kwargs:
            data.update(kwargs)

        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        request = requests.put('{0}/{1}/{2}'.format(self.api_url['publish'],
                               prefix if prefix else '', distr),
                               headers=headers, verify=self.verify_ssl,
                               data=json.dumps(data))
        return response(request)


    def delete_publish(self, distr, **kwargs):
        """Delete published repository, clean up files in published
        directory
        """
        prefix = kwargs.pop('prefix', None)
        if prefix:
            prefix = prefix_sanitized(prefix)

        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.delete('{0}/{1}/{2}'.format(
                                  self.api_url['publish'],
                                  prefix if prefix else '', distr),
                                  params=params, headers=self.headers,
                                  verify=self.verify_ssl)
        return response(request)


    def get_snapshots(self, **kwargs):
        """eturn list of all snapshots created in the system"""
        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.get('{0}'.format(self.api_url['snapshots']),
                               headers=self.headers, params=params,
                               verify=self.verify_ssl)
        return response(request)


    def create_snapshot_from_repo(self, rep_name, **kwargs):
        """Create snapshot of current local repository :name contents
        as new snapshot with name :snapname
        """
        data = {}
        if kwargs:
            data.update(kwargs)

        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        request = requests.post('{0}/{1}/snapshots'.format(
                                self.api_url['repos'], rep_name),
                                headers=headers, verify=self.verify_ssl,
                                data=json.dumps(data))
        return response(request) 


    def create_snapshot_from_pkg(self, **kwargs):
        """Create snapshot from list of package references.

        This API creates snapshot out of any list of package references.
        Package references could be obtained from other snapshots, local
        repos or mirrors.
        """
        data = {}
        if kwargs:
            data.update(kwargs)

        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        request = requests.post('{0}'.format(self.api_url['snapshots']),
                                headers=headers, verify=self.verify_ssl,
                                data=json.dumps(kwargs))
        return response(request)


    def update_snapshot(self, snap_name, **kwargs):
        """Update snapshot's description or name"""
        data = {}
        if kwargs:
            data.update(kwargs)

        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        request = requests.put('{0}/{1}'.format(self.api_url['snapshots'],
                               snap_name), headers=headers,
                               verify=self.verify_ssl, data=json.dumps(data))
        return response(request)


    def show_snapshot(self, snap_name):
        """Get information about snapshot by name"""
        request = requests.get('{0}/{1}'.format(self.api_url['snapshots'],
                               snap_name), headers=self.headers,
                               verify=self.verify_ssl)
        return response(request)


    def delete_snapshot(self, snap_name, **kwargs):
        """Delete snapshot. Snapshot can't be deleted if it is 
        published. Aptly would refuse to delete snapshot if it has
        been used as source to create other snapshots, but that could
        be overridden with force parameter.
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.get('{0}/{1}'.format(self.api_url['snapshots'],
                               snap_name), headers=self.headers, params=params,
                               verify=self.verify_ssl)
        return response(request)


    def show_snapshot_packages(self, snap_name, **kwargs):
        """List all packages in snapshot or perform search on snapshot
        contents and return result.
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.get("{0}/{1}/packages".format(
                               self.api_url['snapshots'], snap_name),
                               params=params, headers=self.headers,
                               verify=self.verify_ssl)
        return response(request)


    def snapshots_diff(self, snapshot1, snapshot2):
        """Calculate difference between two snapshots :snapshot1 (left)
        and :snapshot2 (right).
        """
        request = requests.get("{0}/{1}/diff/{2}".format(
                               self.api_url['snapshots'], snapshot1,
                               snapshot2), headers=self.headers,
                               verify=self.verify_ssl)
        return response(request)


    def aptly_version(self):
        """Return current aptly version"""
        request = requests.get('{0}/version'.format(self.api), 
                               headers=self.headers, verify=self.verify_ssl)
        return response(request) 


    def get_graph(self, ext='png'):
        """Generate graph of aptly objects (same as in aptly graph
        command).
        :param ext: specifies desired file extension, e.g. .png, .svg.
        """
        request = requests.get('{0}/graph.{1}'.format(self.api, ext),
                               headers=self.headers, verify=self.verify_ssl)
        return response(request)
