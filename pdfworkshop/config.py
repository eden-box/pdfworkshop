#!/usr/bin/env python3

import os
import appdirs
import pkg_resources
from configparser import ConfigParser

from ._definitions import CONFIG_FILE


class WorkshopConfig:

    def __init__(self):
        self.__config = self.__load_config()

    @staticmethod
    def __user_config_dir():
        cfg_dir = appdirs.user_config_dir(__name__)
        return os.path.join(cfg_dir, CONFIG_FILE)

    @staticmethod
    def __load_config():
        """
        Load configuration from user ini file
        If it does not exist, a new one is created
        :return: loaded configuration
        """
        parser = ConfigParser()
        cfg_file = WorkshopConfig.__user_config_dir()
        if not os.path.isfile(cfg_file):
            WorkshopConfig.__create_user_config(cfg_file)
        parser.read(cfg_file)
        return parser

    @staticmethod
    def __create_user_config(cfg_file):
        os.makedirs(os.path.dirname(cfg_file), exist_ok=True)
        parser = ConfigParser()
        parser.read_string(pkg_resources.resource_string(__name__, CONFIG_FILE).decode())
        WorkshopConfig.__save_config(parser)

    @staticmethod
    def __save_config(config):
        """
        Save configuration into a file
        :param config: configuration to save
        """
        with open(WorkshopConfig.__user_config_dir(), 'w') as configfile:
            config.write(configfile)

    def list_config(self):
        """
        Lists the ini configuration file
        """
        for section in self.__config.sections():
            print("{}:".format(section))
            for option in self.__config[section]:
                print("  {}: {}".format(option, self.__config.get(section, option)))

    def update_config(self, option, value):
        """
        Update a user config value
        :param option: field to edit
        :param value: new value
        :return: edited config
        """
        if self.__config.has_option("User", option):
            self.__config.set("User", option, value)
            self.__save_config(self.__config)
        return self.__config

    def __get_option(self, option):
        return self.__config.get("User", option, fallback=None)

    def input_dir(self):
        return self.__get_option("input_dir")

    def output_dir(self):
        return self.__get_option("output_dir")

    def public_key(self):
        return self.__get_option("public_key")

    def suffix(self):
        return self.__get_option("suffix")

    def recursive(self):
        return self.__get_option("recursive")
