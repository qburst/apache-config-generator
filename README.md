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

 - Add server_config_generator to the installed app in the settings file, 

```python
	INSTALLED_APPS = (
	# other apps
	"server_config_generator",
    )
```

 - Run **python manage.py generate_apache_config**, 
```bash
	$ python manage.py generate_apache_config 
```
 - User will be prompted to enter the type of virtual hosting, 
```bash
	Please enter name based or IP based hosting (name/ip):?
```
- Enter a valid option and press 'Enter' key
- Then the user will be prompted to enter the server name or the ip address based on the previous input, 
```bash
	Enter the server name:
```
OR
```bash
	Enter your IP: 
```
- Enter a valid server name or ip address
- Then the user will be prompted to enter port number, default value for which will be 80, 
```bash
	Enter the port (default:80):
```
- Enter the required port number and press the 'Enter' key. In the case of the default value just press 'Enter' key
- If STATIC_URL/STATIC_ROOT or MEDIA_URL/MEDIA_ROOT is not configured, then the user will be notified with a warning message and the system will wait for the user confirmation, 
```bash
	Warning: Static root/url not configured
	Warning: Media root/url not configured
	
	 1. Press q to quit 
	 2. Press any key to continue 
```
- Press 'Enter' key to continue, else press "q" and press 'Enter' key
- Then the user will be prompted for https configuration,
```bash
	Do you want https ? 

 	 1. Press 'n' for no 
 	 2. Press any key to continue 
```
- To configure https, user can press on any key else press 'n' and enter key on keyboard
- Then the user will prompted of an automatic redirect from http to https
```bash
	Do you automatic http to https redirect?

	 1. Press 'n' for no 
 	 2. Press any key to continue
```
- To configure autoredirect, user can press on any key else press 'n' and enter key on keyboard
- User will be prompted to enter the path for certificate file
```bash
	Enter certificate path:
```
- After specifying the path to the certificate file, user will be prompted to enter the path to the key file
```bash
	Enter certificate key path:
```
- After specifying the path to the key file, user will be prompted to enter the path to the chain file
```bash
	Enter chain file path or press enter if no chain file
```
- After entering the path to the chain file, user will be prompted to specify the https port
```bash
	Enter the port (default:443):
```
- If a different port is in use than the default port, enter the port and press enter key
- Verify the Apache config file generated in root folder with name as <your_projectname.conf>
- Copy the the conf file to the Apache site-available folder
- Run configtest command
- Enable the site
- Reload Apache
## Communication
- If you **find a bug**, open an issue.
- If you **have a feature request**, open an issue.
- If you **want to contribute**, submit a pull request.

## Author

Afsal Salim, afsals@qburst.com

## License

Django Server Config Generator is available under the MIT license. See the LICENSE file for more info.
