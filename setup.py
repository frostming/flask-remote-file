from setuptools import setup


setup(
    name='flask_remote_file',
    version='0.1.0',
    description='Flask extension to serve remote files via sftp',
    py_modules=['flask_remote_file'],
    url='https://github.com/frostming/flask-remote-file',
    author='Frost Ming',
    author_email='mianghong@gmail.com',
    install_requires=['paramiko', 'flask'],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
