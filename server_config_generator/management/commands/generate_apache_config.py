import sys
import site

from django.core.management import BaseCommand
from django.conf import settings

ANSI_COLOR_START = {
    'INFO': '\033[34m', # Blue Ansi
    'WARNING': '\033[33m', # light yellow background
    'ERROR': '\033[1;31m', #Bold red
}

ANSI_COLOR_END = '\033[0m'

class Command(BaseCommand):
    """
    Management command to create apache config
    """
    help = "Management command to generate apache config automatically"
    
    def handle(self, *args, **options):
        self.log_message("***Start***\n", 'INFO')
        self.get_server_name()
        want_to_continue = self.check_static_and_media_root()
        if not want_to_continue:
            self.log_message('\nPlease add static/media root\n', 'INFO')
            sys.exit()
        self.alias_name = "www." + self.server_name
        self.project_name, _ = settings.SETTINGS_MODULE.split('.')
        self.document_root = settings.BASE_DIR + "/" + self.project_name
        self.path_to_site_packages = sys.prefix + \
            "/lib/python{}.{}/site-packages".format(sys.version_info.major,
                sys.version_info.minor)
        self.generate_conf_file()
        self.log_message(
            "\n***Please verify {}.conf in root folder***\n".format(self.server_name),
            'INFO')

    def log_message(self, message, log_type):
        colored_message = "{}{}{}".format(ANSI_COLOR_START[log_type],
            message, ANSI_COLOR_END)
        sys.stdout.write(colored_message)

    def get_server_name(self):
        self.server_name = None
        while self.server_name is None:
            server_name = input("Enter the server name: ")
            server_name = server_name.strip()
            if not server_name:
                self.log_message("\nServer name is mandatory\n", 'ERROR')
            else:
                self.server_name = server_name

    def check_static_and_media_root(self):
        if not settings.STATIC_ROOT:
            self.log_message("\nWarning: Static root not configured \n", 'WARNING')
        if not settings.MEDIA_ROOT:
            self.log_message("\nWarning: Media root not configured \n", 'WARNING')
        user_input = input("\n 1. Press Q to quit \n 2. Press any key to continue \n")
        if user_input.upper() == "Q":
            return False
        return True

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
