# Flask Remote File

*Flask extension to serve remote files via sftp*

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