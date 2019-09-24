# Django Server Config Generator
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-server-config-generator) ![PyPI - License](https://img.shields.io/pypi/l/django-server-config-generator)

Django server config generator is a simple django extension which generates apache config by running a management command, It automatically detects document root, static root/url, media root/url, and also the path to the current running virtual environment.

## Installation

```bash
$ pip install django-server-config-generator
```

## Requirements
 - Python3.6+
 - Apache2.4
## Usage

 - Add **server_config_generator** in your installed app in settings file

```python
	INSTALLED_APPS = (
	# other apps
	"server_config_generator",
    )
```

 - Run **python manage.py generate_apache_config**
```bash
	$ python manage.py generate_apache_config 
```
 - User will be prompted to enter type of virtualhosting ie namebase or ipbased
```bash
	Please enter name based or IP based hosting (name/ip):?
```
- Enter a valid option and press enter
- Then user will be prompted to enter either servername or ip based on the previous input
```bash
	Enter the server name:
```
OR
```bash
	Enter your IP: 
```
- Enter valid servername or ip address
- Then user will be prompted to enter portnumber, default will be 80
```bash
	Enter the port (default:80):
```
- Enter required port and press enter incase of default just press enter
-  If STATIC_URL/STATIC_ROOT or MEDIA_URL/MEDIA_ROOT not configured user will notified with a warning message and wait for user confirnamtion
```bash
	Warning: Static root/url not configured
	Warning: Media root/url not configured
	
	 1. Press q to quit 
	 2. Press any key to continue 
```
- Press Enter to continue else press "q" and press enter
 - Verify the apache config file generated in root folder with name as <your_projectname.conf>
 - Copy the the conf file to apache site-available folder
 - Check configuration using apache command
 - Enable site
 - Reload apache
## Communication
- If you **found a bug**, open an issue.
- If you **have a feature request**, open an issue.
- If you **want to contribute**, submit a pull request.

## Author

Afsal Salim, afsals@qburst.com

## License

Django Server Config Generator is available under the MIT license. See the LICENSE file for more info.
