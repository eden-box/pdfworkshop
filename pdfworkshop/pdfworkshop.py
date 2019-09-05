#!/usr/bin/env python3

import os
import glob
import zipfile

from pylovepdf.tools.compress import Compress
from .config import WorkshopConfig as Config


class PDFWorkshop:

    def __init__(self):

        # load configuration
        self.__config = Config()

    @staticmethod
    def __setup_dir(directory_path):
        """
        Creates a directory if it does not exist
        :param directory_path: directory to setup up
        """
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

    @staticmethod
    def __clean_filename(filename):
        """
        Simple way to rename compressed file to the original file name
        It is not a full proof detection method, but it will hardly present any issue
        :param filename: file path to adapt
        :return: adapted file path
        """
        return "{}.pdf".format(filename.split("_compress_", 1)[0])

    @staticmethod
    def __get_files(directory, file_extension):
        """
        Get a list of all files of a given type in a directory
        :param directory: directory to search
        :param file_extension: file extension to search
        :return: list of found files
        """
        return glob.glob("{}*.{}".format(directory, file_extension))

    @staticmethod
    def __get_files_to_rename(directory):
        """
        Get list of recently compressed files, to rename
        :param directory: directory where the compressed files were stored
        :return: files to rename
        """
        return [file for file in PDFWorkshop.__get_files(directory, "pdf") if "_compress_" in file]

    def setup(self, option, value):
        """
        Edit a user configuration
        :param option: option to edit
        :param value: new value
        """
        self.__config.update_config(option, value)

    def list_config(self):
        """
        List user configurations
        """
        self.__config.list_config()

    def run(self):
        """
        Run using the stored configurations
        """
        self.__run(
            self.__config.public_key(),
            self.__config.input_dir(),
            self.__config.output_dir()
        )

    def __run(self, public_key, input_dir, output_dir):
        """
        Compress PDF files stored in input_dir and store the resultant files in output_dir
        Authentication is made using the provided public key
        :param public_key: API development public key
        :param input_dir: directory where the PDF files will be collected from
        :param output_dir: directory where the compressed PDF files will be stored
        """

        # create directories if they do not exist
        self.__setup_dir(self.__config.input_dir())
        self.__setup_dir(self.__config.output_dir())

        compress = Compress(public_key, verify_ssl=True)
        compress.set_output_folder(output_dir)

        # search current directory
        [compress.add_file(file) for file in self.__get_files(input_dir, "pdf")]

        compress.execute()  # upload files to iLovePDF
        compress.download()  # download resultant file

        # unzip response zip, if there is one
        # note that the API response is a zip only if more than one pdf was submitted
        for zip_file in PDFWorkshop.__get_files(output_dir, "zip"):
            zip_ref = zipfile.ZipFile(zip_file, 'r')
            zip_ref.extractall(output_dir)
            zip_ref.close()
            os.remove(zip_file)

        # rename all pdf to their original filename
        [os.rename(filename, PDFWorkshop.__clean_filename(filename))
         for filename in PDFWorkshop.__get_files_to_rename(output_dir)]
