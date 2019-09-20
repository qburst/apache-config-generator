import sys
import site

from django.core.management import BaseCommand
from django.conf import settings

from server_config_generator.coloured_sys_out import ColouredSysOut

class Command(BaseCommand):
    """
    Management command to create apache config
    """
    help = "Management command to generate apache config automatically"
    
    def handle(self, *args, **options):
        """
        Django handle method
        """
        ColouredSysOut.log_message("***Start***", 'blue')
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
        ColouredSysOut.log_message("***Please verify {}.conf in root folder***".format(
            self.server_name), "blue")

    def get_server_name(self):
        """
        Method to recieve server name from the user
        @params: Instance
        @return None
        Wait until user inputs servername
        """
        self.server_name = None
        while self.server_name is None:
            server_name = input("Enter the server name: ")
            server_name = server_name.strip()
            if not server_name:
                ColouredSysOut.log_message("Server name is mandatory", "red")
            else:
                self.server_name = server_name

    def check_static_and_media_root(self):
        """
        Method to check if user static root and media root is configured
        @params: Instance
        @return: Boolean, True if both static and media root configured
        """
        has_warning = False
        if not settings.STATIC_ROOT:
            ColouredSysOut.log_message("Warning: Static root not configured", "yellow")
            has_warning = True
        if not settings.MEDIA_ROOT:
            ColouredSysOut.log_message("Warning: Media root not configured", "yellow")
            has_warning = True
        if not has_warning:
            return True
        user_input = input("\n 1. Press Q to quit \n 2. Press any key to continue \n")
        if user_input.upper() == "Q":
            return False
        return True

    def generate_conf_file(self):
        """
        Method to generate config file with servername
        @params: Instance
        @return: None
        Generates conf file with given servername in root folder
        ie if servername is test then test.conf is generated in root folder
        """
        with open(self.server_name + '.conf', 'w+') as config_file:
            config_file.writelines("<VirtualHost *:80>\n")
            config_file.writelines(f"\tServerName {self.server_name}\n")
            config_file.writelines(f"\tServerAlias {self.alias_name}\n")
            config_file.writelines(f"\tDocumentRoot {self.document_root}\n\n")
            if settings.STATIC_ROOT:
                config_file.writelines(
                    f"\tAlias {settings.STATIC_URL} {settings.STATIC_ROOT}/ \n")
                config_file.writelines(f"\t<Directory {settings.STATIC_ROOT}>\n")
                config_file.writelines(f"\t\tRequire all granted\n")
                config_file.writelines(f"\t</Directory>\n\n")
            if settings.MEDIA_ROOT:
                config_file.writelines(
                    f"\tAlias {settings.MEDIA_URL} {settings.MEDIA_ROOT}/ \n")
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
