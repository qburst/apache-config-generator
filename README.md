# Django Server Config Generator
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-server-config-generator) ![PyPI - License](https://img.shields.io/pypi/l/django-server-config-generator)

Django server config generator is a simple django extension which generate apache config by running a management command, It automatically detect document root, static root/url, media root/url, also path to current running virtualenvironment

## Installation
$ pip install django-server-config-generator

## Requirements
Python3.6+
## Usage

 - Add **server_config_generator** in your installed app
 - Run **python manage.py generate_apache_config**
 - User will prompt for servername and some confirmations, enter those details
 - Verify <server_name>.conf is generated in the root folder, server_name is given by user in previous step
 - Enable site using this configuration and restart apache
## Communication
- If you **found a bug**, open an issue.
- If you **have a feature request**, open an issue.
- If you **want to contribute**, submit a pull request.

## Author

Afsal Salim, afsals@qburst.com

## License

Django Server Config Generator is available under the MIT license. See the LICENSE file for more info.
