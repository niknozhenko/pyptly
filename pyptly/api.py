import json
import requests
from base64 import b64encode
from pyptly.utils import prefix_sanitized, response

class Aptly(object):
    """Aptly class"""

    def __init__(self, host, user=None, password=None, verify_ssl=True,
                 timeout = 90):
        self.timeout = timeout
        self.headers = {}
        if user and password:
            self.headers['Authorization'] = b'Basic ' + b64encode(
                                str.encode(user) + b':' + str.encode(password))
        if not host:
            raise ValueError('host argument may not be empty')
        self.host = host.rstrip('/')
        if self.host.startswith('http://') or self.host.startswith('https://'):
            pass
        else:
            self.host = 'http://' + self.host

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
                               timeout=self.timeout,
                               headers=self.headers,
                               verify=self.verify_ssl)
        return response(request)


    def create_local_repo(self, name, **kwargs):
        """Create empty local repository with specified parameters

        :param name: name of the new local repository
        :param **kwargs: all parameters allowed by Aptly API
        """
        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        data = {'Name': name}
        if kwargs:
            data.update(kwargs)

        request = requests.post("{0}".format(self.api_url['repos']),
                                data=json.dumps(data),
                                headers=headers,
                                timeout=self.timeout,
                                verify=self.verify_ssl)
        return response(request)


    def show_local_repo(self, name):
        """Returns basic information about local repository
        :param name: name of the new local repository
        """
        request = requests.get("{0}/{1}".format(self.api_url['repos'], name),
                               headers=self.headers,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def show_repo_packages(self, name, **kwargs):
        """List all packages in local repository or perform search on
        repository contents and return result
        :param name: name of the local repository
        :param **kwargs: all parameters allowed by Aptly API
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.get('{0}/{1}/packages'.format(self.api_url['repos'],
                                                         name),
                               timeout=self.timeout,
                               params=params,
                               headers=self.headers,
                               verify=self.verify_ssl)
        return response(request)


    def edit_local_repo(self, name, **kwargs):
        """Update local repository meta information

        :param name: name of the local repository
        :param **kwargs: all parameters allowed by Aptly API
        """
        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        data = {}
        if kwargs:
            data.update(kwargs)

        request = requests.put('{0}/{1}'.format(self.api_url['repos'], name),
                               data=json.dumps(data),
                               headers=headers,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def delete_local_repo(self, name, **kwargs):
        """Delete local repository. Local repository can't be deleted
        if it is published. If local repository has snapshots, aptly
        would refuse to delete it by default, but that can be overridden
        with force flag

        :param name: name of the local repository
        :param **kwargs: all parameters allowed by Aptly API
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.delete('{0}/{1}'.format(self.api_url['repos'],
                                                   name),
                                  headers=self.headers,
                                  verify=self.verify_ssl,
                                  timeout=self.timeout,
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
        :param filename: name of the file to add
        :param **kwargs: all parameters allowed by Aptly API
        """

        filename = kwargs.pop('filename', None)
        params = {}
        if kwargs:
            params.update(kwargs)

        if filename:
            request = requests.post('{0}/{1}/file/{2}/{3}'.format(
                                                    self.api_url['repos'],
                                                    name, dirname, filename),
                                    timeout=self.timeout,
                                    headers=self.headers,
                                    verify=self.verify_ssl, params=params)
        else:
            request = requests.post('{0}/{1}/file/{2}'.format(
                                                    self.api_url['repos'],
                                                    name, dirname),
                                    headers=self.headers,
                                    verify=self.verify_ssl, params=params)
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
        :param **kwargs: all parameters allowed by Aptly API
        """
        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        data = {}
        if kwargs:
            data.update(kwargs)

        request = requests.post('{0}/{1}/packages'.format(self.api_url['repos'],
                                                          name),
                                data=json.dumps(data),
                                headers=headers,
                                timeout=self.timeout,
                                verify=self.verify_ssl)
        return response(request)


    def delete_pkg_bykey(self, name, **kwargs):
        """Remove packages from local repository by package keys.

        Any package(s) could be removed from local repository. List
        package references in local repository could be retrieved with
        show_repo_packages

        :param name: name of the local repository
        :param **kwargs: all parameters allowed by Aptly API
        """
        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        data = {}
        if kwargs:
            data.update(kwargs)

        request = requests.delete('{0}/{1}/packages'.format(
                                  self.api_url['repos'], name),
                                  data=json.dumps(data),
                                  headers=headers,
                                  timeout=self.timeout,
                                  verify=self.verify_ssl)
        return response(request)


    def show_pkg_bykey(self, key):
        """Show information about package by package key.
        Package keys could be obtained from various
        GET .../packages APIs.

        :param key: package key
        """
        request = requests.get('{0}/{1}'.format(self.api_url['packages'],
                                                key),
                               headers=self.headers,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def get_dirs(self):
        """List all directories"""
        request = requests.get('{0}'.format(self.api_url['files']),
                               headers=self.headers,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def get_files(self, dirname):
        """Returns list of files in directory

        :param dirname: directory name to inspect
        """
        request = requests.get('{0}/{1}'.format(self.api_url['files'],
                                                dirname),
                               headers=self.headers,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def delete_dir(self, dirname):
        """Deletes all files in upload directory and directory itself

        :param dirname: directory name to delete
        """
        request = requests.delete('{0}/{1}'.format(self.api_url['files'],
                                                   dirname),
                                  headers=self.headers,
                                  timeout=self.timeout,
                                  verify=self.verify_ssl)
        return response(request)


    def delete_file(self, dirname, filename):
        """Delete single file in directory

        :param dirname: directory to delete from
        :param filename: file to delete
        """
        request = requests.delete('{0}/{1}/{2}'.format(self.api_url['files'],
                                                       dirname, filename),
                                  headers=self.headers,
                                  timeout=self.timeout,
                                  verify=self.verify_ssl)
        return response(request)


    def upload_files(self, dirname, files):
        """Parameter :dir is upload directory name. Directory would be
        created if it doesn't exist.

        Any number of files can be uploaded in one call, aptly would
        preserve filenames. No check is performed if existing uploaded
        would be overwritten.

        :param dirname: upload directory name
        :param files: files to upload. Single file path or list of pathes.
        """
        if isinstance(files, list):
            files = [('file', open(f, 'rb')) for f in files]
        else:
            files = {'file': open(files, 'rb')}

        request = requests.post('{0}/{1}'.format(self.api_url['files'],
                                                 dirname),
                                files=files,
                                headers=self.headers,
                                timeout=self.timeout,
                                verify=self.verify_ssl)
        return response(request)


    def get_publish(self):
        """List published repositories"""
        request = requests.get('{0}'.format(self.api_url['publish']),
                               headers=self.headers,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def publish(self, **kwargs):
        """Publish local repository or snapshot under specified prefix.
        Storage might be passed in prefix as well, e.g. s3:packages/.

        :param **kwargs: all parameters allowed by Aptly API
        """
        prefix = kwargs.pop('prefix', None)
        if prefix:
            prefix = prefix_sanitized(prefix)

        data = kwargs
        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        request = requests.post('{0}/{1}'.format(self.api_url['publish'],
                                                 prefix if prefix else ''),
                                headers=headers,
                                timeout=self.timeout,
                                data=json.dumps(data),
                                verify=self.verify_ssl)
        return response(request)


    def update_publish(self, distr, **kwargs):
        """API action depends on published repository contents:
        * if local repository has been published, published repository
        would be updated to match local repository contents
        * if snapshots have been been published, it is possible to
        switch each component to new snapshot

        :param **kwargs: all parameters allowed by Aptly API
        """
        prefix = kwargs.pop('prefix', None)
        if prefix:
            prefix = prefix_sanitized(prefix)

        data = {}
        if kwargs:
            data.update(kwargs)

        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        request = requests.put('{0}/{1}/{2}'.format(self.api_url['publish'],
                                                    prefix if prefix else '',
                                                    distr),
                               timeout=self.timeout,
                               headers=headers,
                               verify=self.verify_ssl,
                               data=json.dumps(data))
        return response(request)


    def delete_publish(self, distr, **kwargs):
        """Delete published repository, clean up files in published
        directory

        :param **kwargs: all parameters allowed by Aptly API
        """
        prefix = kwargs.pop('prefix', None)
        if prefix:
            prefix = prefix_sanitized(prefix)

        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.delete('{0}/{1}/{2}'.format(self.api_url['publish'],
                                                       prefix if prefix else '',
                                                       distr),
                                  params=params,
                                  timeout=self.timeout,
                                  headers=self.headers,
                                  verify=self.verify_ssl)
        return response(request)


    def get_snapshots(self, **kwargs):
        """Return list of all snapshots created in the system

        :param **kwargs: all parameters allowed by Aptly API
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.get('{0}'.format(self.api_url['snapshots']),
                               headers=self.headers,
                               params=params,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def create_snapshot_from_repo(self, rep_name, **kwargs):
        """Create snapshot of current local repository :name contents
        as new snapshot with name :snapname

        :param **kwargs: all parameters allowed by Aptly API
        """
        data = {}
        if kwargs:
            data.update(kwargs)

        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        request = requests.post('{0}/{1}/snapshots'.format(self.api_url['repos'],
                                                           rep_name),
                                headers=headers,
                                verify=self.verify_ssl,
                                timeout=self.timeout,
                                data=json.dumps(data))
        return response(request)


    def create_snapshot_from_pkg(self, **kwargs):
        """Create snapshot from list of package references.

        This API creates snapshot out of any list of package references.
        Package references could be obtained from other snapshots, local
        repos or mirrors.

        :param **kwargs: all parameters allowed by Aptly API
        """
        data = {}
        if kwargs:
            data.update(kwargs)

        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        request = requests.post('{0}'.format(self.api_url['snapshots']),
                                headers=headers,
                                verify=self.verify_ssl,
                                timeout=self.timeout,
                                data=json.dumps(kwargs))
        return response(request)


    def update_snapshot(self, snap_name, **kwargs):
        """Update snapshot's description or name

        :param **kwargs: all parameters allowed by Aptly API
        """
        data = {}
        if kwargs:
            data.update(kwargs)

        headers = dict({'Content-Type': 'application/json'}, **self.headers)
        request = requests.put('{0}/{1}'.format(self.api_url['snapshots'],
                                                snap_name),
                               headers=headers,
                               verify=self.verify_ssl,
                               timeout=self.timeout,
                               data=json.dumps(data))
        return response(request)


    def show_snapshot(self, snap_name):
        """Get information about snapshot by name"""
        request = requests.get('{0}/{1}'.format(self.api_url['snapshots'],
                                                snap_name),
                               headers=self.headers,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def delete_snapshot(self, snap_name, **kwargs):
        """Delete snapshot. Snapshot can't be deleted if it is
        published. Aptly would refuse to delete snapshot if it has
        been used as source to create other snapshots, but that could
        be overridden with force parameter.

        :param **kwargs: all parameters allowed by Aptly API
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.delete('{0}/{1}'.format(self.api_url['snapshots'],
                                                snap_name),
                               headers=self.headers,
                               params=params,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def show_snapshot_packages(self, snap_name, **kwargs):
        """List all packages in snapshot or perform search on snapshot
        contents and return result.

        :param **kwargs: all parameters allowed by Aptly API
        """
        params = {}
        if kwargs:
            params.update(kwargs)

        request = requests.get("{0}/{1}/packages".format(
                               self.api_url['snapshots'], snap_name),
                               params=params,
                               headers=self.headers,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def snapshots_diff(self, snapshot1, snapshot2):
        """Calculate difference between two snapshots :snapshot1 (left)
        and :snapshot2 (right).
        """
        request = requests.get("{0}/{1}/diff/{2}".format(
                               self.api_url['snapshots'], snapshot1,
                               snapshot2),
                               headers=self.headers,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def aptly_version(self):
        """Return current aptly version"""
        request = requests.get('{0}/version'.format(self.api),
                               headers=self.headers,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        return response(request)


    def get_graph(self, path='', ext='png'):
        """Generate graph of aptly objects (same as in aptly graph
        command).

        :param path: file path for graph
        :param ext: specifies desired file extension, e.g. .png, .svg.
        """
        path = path if path else 'graph.' + ext
        request = requests.get('{0}/graph.{1}'.format(self.api, ext),
                               headers=self.headers,
                               timeout=self.timeout,
                               verify=self.verify_ssl)
        if request.status_code == 200:
            with open(path, 'wb') as file_pointer:
                for chunk in request:
                    file_pointer.write(chunk)

        return {'Path': path}
