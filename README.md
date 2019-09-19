# Django Server Config Generator
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-server-config-generator) ![PyPI - License](https://img.shields.io/pypi/l/django-server-config-generator)

Django server config generator is a simple django extension which generates apache config by running a management command, It automatically detects document root, static root/url, media root/url, and also the path to the current running virtual environment.

## Installation
$ pip install django-server-config-generator

## Requirements
Python3.6+
Apache2.4
## Usage

 - Add **server_config_generator** in your installed app
 - Run **python manage.py generate_apache_config**
 - User will be prompted to enter the server name and make some confirmations
 - Verify if <server_name>.conf is generated in the root folder, server_name is entered by the user in the previous step
 - Enable site using this configuration and restart apache
## Communication
- If you **found a bug**, open an issue.
- If you **have a feature request**, open an issue.
- If you **want to contribute**, submit a pull request.

## Author

Afsal Salim, afsals@qburst.com

## License

Django Server Config Generator is available under the MIT license. See the LICENSE file for more info.
