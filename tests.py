"""
    flask_remote_file test suite
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: Frost Ming
    :email: mianghong@gmail.com
    :license: MIT
"""
import os.path as op
import pytest
from flask import Flask
from flask_remote_file import RemoteFile

try:
    import unittest.mock as mock
except ImportError:
    import mock

here = op.dirname(__file__)


def mock_ssh_client():
    def mock_open(filepath, mode='r', buffsize=-1):
        return open(filepath, mode, buffsize)

    client = mock.Mock()
    client.open_sftp.return_value.open.side_effect = mock_open
    return client


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr('paramiko.SSHClient', mock_ssh_client)
    app = Flask(__name__)
    bp = RemoteFile('remote', op.join(here, 'fixtures'), 'localhost')
    bp_sub = RemoteFile('remote_sub', op.join(here, 'fixtures', 'subfolder'),
                        'localhost')
    app.register_blueprint(bp, url_prefix='/remote')
    app.register_blueprint(bp_sub, url_prefix='/remote_sub')
    app.testing = True
    return app.test_client()


def test_file_types(client):
    rv = client.get('/remote/test_txt.txt')
    assert 'text/plain' in rv.mimetype
    assert rv.data == open('fixtures/test_txt.txt', 'rb').read()

    rv = client.get('/remote/test_excel.xlsx')
    assert rv.is_streamed
    assert 'application/vnd.openxmlformats' in rv.mimetype

    rv = client.get('/remote/flask.png')
    assert 'image/x-png' in rv.mimetype or 'image/png' in rv.mimetype


def test_two_blueprints(client):
    rv = client.get('/remote_sub/test_txt.txt')
    assert 'text/plain' in rv.mimetype
    assert rv.data == open('fixtures/subfolder/test_txt.txt', 'rb').read()

    rv = client.get('/remote_sub/requests.png')
    assert 'image/x-png' in rv.mimetype or 'image/png' in rv.mimetype

    rv = client.get('/remote/subfolder/requests.png')
    assert 'image/x-png' in rv.mimetype or 'image/png' in rv.mimetype

    rv = client.get('/remote/non_exist.txt')
    assert rv.status_code == 404


def test_secure_path(client):
    rv = client.get('/remote/subfolder/../test_txt.txt')
    assert rv.status_code == 200

    rv = client.get('/remote/subfolder/../../README.md')
    assert rv.status_code == 404
