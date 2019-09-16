
Django Server Config Generator
=====

Django Server Config Generator is a django extension to generate Apache config just by running a management command.

Quick start
-----------

Quick start
1. Add "server_config_generator" to your INSTALLED_APPS
INSTALLED_APPS = [ ... 'server_config_generator', ]

2. Run python manage.py generate_apache_config
Enter your server name on user prompt

3. Verify apacheconfig file generated in root folder
