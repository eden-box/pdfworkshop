#!/usr/bin/env python3

import os
import appdirs
import pkg_resources
from configparser import ConfigParser

from ._definitions import CONFIG_FILE, USER_SECTION


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
        WorkshopConfig.__update_user_config(cfg_file)
        parser.read(cfg_file)
        return parser

    @staticmethod
    def __update_user_config(cfg_file):
        """
        Create or update user configuration file
        If it does not exist, a new one os created
        If it does exist, it is verified if the base configuration requires an update,
        which is applied while retaining the previous user configuration
        :param cfg_file: path to configuration file
        """
        parser = ConfigParser()
        parser.read_string(pkg_resources.resource_string(__name__, CONFIG_FILE).decode())
        if not os.path.isfile(cfg_file):  # create a new configuration file
            os.makedirs(os.path.dirname(cfg_file), exist_ok=True)
            WorkshopConfig.__save_config(parser)
        else:  # verify if an update is needed and apply it
            prev_parser = ConfigParser()
            prev_parser.read(cfg_file)
            if parser[USER_SECTION] != prev_parser[USER_SECTION]:
                parser.remove_section(USER_SECTION)
                parser[USER_SECTION] = prev_parser[USER_SECTION]
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
        if self.__config.has_option(USER_SECTION, option):
            self.__config.set(USER_SECTION, option, value)
            self.__save_config(self.__config)
        return self.__config

    def __get_section(self):
        return self.__config[USER_SECTION]

    def input_dir(self):
        return self.__config.get(USER_SECTION, "input_dir")

    def output_dir(self):
        return self.__config.get(USER_SECTION, "output_dir")

    def public_key(self):
        return self.__config.get(USER_SECTION, "public_key")

    def suffix(self):
        return self.__config.get(USER_SECTION, "suffix")

    def recursive(self):
        return self.__config.getboolean(USER_SECTION, "recursive")
