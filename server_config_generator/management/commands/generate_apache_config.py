import sys
import site

from django.core.management import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """
    Management command to create apache config
    """
    help = "Management command to generate apache config automatically"
    
    def handle(self, *args, **options):
        self.stdout.write("Start *************************")
        self.get_server_name()
        self.alias_name = "www." + self.server_name
        self.project_name, _ = settings.SETTINGS_MODULE.split('.')
        self.document_root = settings.BASE_DIR + "/" + self.project_name
        self.path_to_site_packages = sys.prefix + \
            "/lib/python{}.{}/site-packages".format(sys.version_info.major,
                sys.version_info.minor)
        self.generate_conf_file()
        self.stdout.write("Completed**********************")


    def get_server_name(self):
        self.server_name = None
        while self.server_name is None:
            server_name = input("Enter the server name: ")
            server_name = server_name.strip()
            if not server_name:
                self.stdout.write("\nServer name is mandatory\n")
            else:
                self.server_name = server_name


    def generate_conf_file(self):
        with open(self.server_name + '.conf', 'w+') as config_file:
            config_file.writelines("<VirtualHost *:80>\n")
            config_file.writelines(f"\tServerName {self.server_name}\n")
            config_file.writelines(f"\tServerAlias {self.alias_name}\n")
            config_file.writelines(f"\tDocumentRoot {self.document_root}\n")
            if settings.STATIC_ROOT:
                config_file.writelines(
                    f"\tAlias {settings.STATIC_URL} {settings.STATIC_ROOT}\n")
            if settings.MEDIA_ROOT:
                config_file.writelines(
                    f"\tAlias {settings.MEDIA_URL} {settings.MEDIA_ROOT}\n")
            config_file.writelines("\n")
            if settings.STATIC_ROOT:
                config_file.writelines(f"\t<Directory {settings.STATIC_ROOT}>\n")
                config_file.writelines(f"\t\tRequire all granted\n")
                config_file.writelines(f"\t</Directory>\n\n")
            if settings.MEDIA_ROOT:
                config_file.writelines(f"\t<Directory {settings.MEDIA_ROOT}>\n")
                config_file.writelines(f"\t\tRequire all granted\n")
                config_file.writelines(f"\t</Directory>\n\n")

            config_file.writelines(f"\t<Directory {self.document_root}>\n")
            config_file.writelines(f"\t\t<Files wsgi.py>\n")
            config_file.writelines(f"\t\t\tRequire all granted\n")
            config_file.writelines(f"\t\t</Files>\n")
            config_file.writelines(f"\t</Directory>\n\n")

            config_file.writelines(f"\tWSGIDaemonProcess {self.server_name} " + \
                f"python-path={settings.BASE_DIR}:{self.path_to_site_packages}\n\n")
            config_file.writelines(f"\tWSGIProcessGroup {self.server_name}\n")
            config_file.writelines(f"\tWSGIScriptAlias / {self.document_root}/wsgi.py\n\n")
            config_file.writelines("</VirtualHost>\n")

