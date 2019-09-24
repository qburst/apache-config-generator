import sys
import re
import os

from django.core.management import BaseCommand
from django.conf import settings
from django.template.loader import get_template 

from server_config_generator.coloured_sys_out import ColouredSysOut


class Command(BaseCommand):
    """
    Management command to create apache config
    """
    static_url = settings.STATIC_URL
    static_root = settings.STATIC_ROOT
    media_url = settings.MEDIA_URL
    media_root = settings.MEDIA_ROOT
    base_dir = settings.BASE_DIR

    help = "Management command to generate apache config automatically"

    def handle(self, *args, **options):
        """
        Django handle method for management command
        """
        ColouredSysOut.log_message("***Start***", 'blue')
        self.get_server_name_or_ip()
        self.get_port()
        is_static_and_media_configured = self.check_static_and_media_root_configured()
        if not is_static_and_media_configured:
            user_input = input("\n 1. Press q to quit \n 2. Press any key to continue \n")
            if self.validate_input_with_pre_defined_options(user_input, "q"):
                sys.exit()
        self.project_name, _ = settings.SETTINGS_MODULE.split('.')
        self.document_root = settings.BASE_DIR + "/" + self.project_name
        self.path_to_site_packages = sys.prefix + \
            "/lib/python{}.{}/site-packages".format(sys.version_info.major,
                sys.version_info.minor)
        self.generate_conf_file()
        ColouredSysOut.log_message("***Please verify {}.conf in root folder***".format(
            self.project_name), "blue")

    @staticmethod
    def validate_input_with_pre_defined_options(user_input, valid_options):
        """
        Method to check where use input in a valid option
        @params user_input: Input from user
        @params valid_options: Array of valid options
        @return Boolean: True, if input is valid else false
        """
        if user_input:
            user_input = user_input.lower()
            return user_input in valid_options
        return False

    @staticmethod
    def validate_ip_address(user_input):
        """
        Method to check given input is valid ip
        @params user_input: Input from user
        @return Boolean: True, if it is valid ip else return false
        """
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", user_input):
            return True
        return False

    def get_server_name_or_ip(self):
        """
        Method to recieve server name from the user
        @params self: Instance
        @return None
        Wait until user inputs servername
        """
        self.server_name = None
        self.ip = None
        self.ip_or_server_name = None
        while self.ip_or_server_name is None:
            user_input = input("Please enter name based or IP based hosting "+\
                "(name/ip):?")
            if self.validate_input_with_pre_defined_options(user_input, ['ip', 'name']):
                self.ip_or_server_name = user_input
        while (self.server_name is None and self.ip is None):
            if self.ip_or_server_name == "name":
                server_name = input("Enter the server name: ")
                server_name = server_name.strip()
                if not server_name:
                    ColouredSysOut.log_message("Please enter servername", "red")
                else:
                    self.server_name = server_name
            else:
                ip = input("Enter your IP: ")
                ip = ip.strip()
                if not self.validate_ip_address(ip):
                    ColouredSysOut.log_message("Please enter valid IP", "red")
                else:
                    self.ip = ip

    @staticmethod
    def validate_port(user_input):
        """
        Method to validate port number
        @params user_input: Input from user
        @return Boolean True, if input is valid port else False
        """
        try:
            port_number = int(user_input)
            return 1 <= port_number <= 65535
        except ValueError:
            return False

    def get_port(self):
        """
        Method to recieve port from user
        @params self: Instance
        @return None
        """
        self.port = None
        while self.port is None:
            user_input = input("\nEnter the port (default:80):")
            if not user_input:
                self.port = 80
            elif not self.validate_port(user_input):
                ColouredSysOut.log_message("Please enter valid Port", "red")
            else:
                self.port = int(user_input)

    def check_static_and_media_root_configured(self):
        """
        Method to check if user static root and media root is configured
        @params self: Instance
        @return Boolean, True if both static and media root configured
        """
        is_configured = True
        if not (self.static_url and self.static_root):
            ColouredSysOut.log_message("Warning: Static root/url not configured", "yellow")
            is_configured = False
        if not (self.media_url and self.media_root):
            ColouredSysOut.log_message("Warning: Media root/url not configured", "yellow")
            has_warning = False
        return is_configured

    def generate_conf_file(self):
        """
        Method to generate config file with servername
        @params self: Instance
        @return None
        Generates conf file with your django project name root folder
        ie if project name is test then test.conf is generated in root folder
        """
        template = get_template('apache/apache_http_only.tmpl')
        content = template.render({"obj": self})
        split = content.split('\n')
        split = list(filter(None, split))
        content = "\n\n".join(split)
        with open(self.project_name + ".conf" , 'w+') as config_file:
            config_file.writelines(content)
