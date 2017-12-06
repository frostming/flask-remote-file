"""
    flask_remote_file
    ~~~~~~~~~~~~~~~~~
    Flask extension to serve remote files via sftp

    :author: Frost Ming
    :email: mianghong@gmail.com
    :license: MIT
"""
import os.path as op
import paramiko
from flask import Blueprint, g, request, send_file
from werkzeug.exceptions import NotFound
import logging


class RemoteFile(Blueprint):
    """A `flask.Blueprint` subclass that serves remote files

    :param name: the blueprint name
    :param fileroot: the root of remote files
    :param hostname: the remote server hostname
    :param port: the remote server port
    :param username: the username used to connect to remote server
    :param password: the password used to connect to remote server
    :param url_prefix: the url prefix of the blueprint
    :param subdomain: the subdomain of the blueprint
    :param \**kwargs: other options passed to `SSHClient.connect()`
    """
    def __init__(self, name, fileroot, hostname, port=22, username=None,
                 password=None, url_prefix=None,
                 subdomain=None, **kwargs):
        Blueprint.__init__(self, name, __name__, url_prefix=url_prefix,
                           subdomain=subdomain)
        self.fileroot = fileroot
        self.ssh_options = {
            'hostname': hostname,
            'port': port,
            'username': username, 
            'password': password,
        }
        self.ssh_options.update(kwargs)
        self.setup_views()

    def setup_views(self):
        self.before_request(self.get_sftp)
        self.record_once(lambda s: s.app.teardown_appcontext_funcs
                         .append(self.close_sftp))
        self.add_url_rule('/<path:filepath>', 'remote_file', self.get_file)

    def get_sftp(self):
        ssh_client = g.get('ssh_%s' % self.name, None)
        if ssh_client is None:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(**self.ssh_options)
            g.setdefault('ssh_%s' % self.name, ssh_client)
        sftp = g.get('sftp_%s' % self.name, None)
        if sftp is None or sftp.sock.closed:
            g.setdefault('sftp_%s' % self.name, ssh_client.open_sftp())

    def close_sftp(self, exc=None):
        ssh_client = g.pop('ssh_%s' % self.name, None)
        if ssh_client is not None:
            ssh_client.close()
        g.pop('sftp_%s' % self.name, None)

    def get_file(self, filepath):
        full_path = op.abspath(op.join(self.fileroot, filepath))
        if full_path[:len(self.fileroot)] != self.fileroot:
            raise NotFound()
        try:
            fp = g.get('sftp_%s' % self.name).open(full_path)
        except IOError:
            raise NotFound()
        as_attachment = request.args.get('attachment') == '1'
        filename = op.basename(full_path)
        return send_file(fp, None, as_attachment, filename, False)
