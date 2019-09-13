=====
Django Server Config Generator
=====

Django Server Config Generator is a django extension for generate 
Apache config with just running a management command

Quick start
-----------

1. Add "server_config_generator" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'server_config_generator',
    ]


2. Run `python manage.py generate_apache_config`, user get a prompt for enter server name
3. Enter server name then apacheconfig for the site will be created in root folder


