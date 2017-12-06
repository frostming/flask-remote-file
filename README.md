# Flask Remote File
[![Build Status](https://travis-ci.org/frostming/flask-remote-file.svg?branch=master)](https://travis-ci.org/frostming/flask-remote-file)

*Flask extension to serve remote files via sftp*

## Why we need this

Sometimes we want to access remote files via SFTP but the SFTP server is not exposed to current client or we want to limit the accessible scope. **flask_remote_file** will help setup a flask app to forward the request to SFTP server and prevent any illegal access.

## Installation:
```bash
$ pip install flask-remote-file
```

## Usage:
```python
from flask import Flask
from flask_remote_file import RemoteFile
app = Flask(__name__)
bp = RemoteFile('dev', '/home/fming/static_files', 'myserver.org')
app.register_blueprint(bp, url_prefix='/remote')
```