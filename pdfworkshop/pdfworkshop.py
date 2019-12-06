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
        Creates a directory if it does not exist.
        :param directory_path: directory to setup up
        """
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)

    @staticmethod
    def __rename_file(filename, suffix):
        """
        Rename a compressed file to the original filename and possibly add a suffix.
        :param filename: filename to adapt
        :param suffix: suffix given to the compressed file (before the extension)
        :return: new filename
        """
        filename = PDFWorkshop.__clean_filename(filename)
        return PDFWorkshop.__add_filename_suffix(filename, suffix)

    @staticmethod
    def __add_filename_suffix(filename, suffix):
        """
        Add a suffix to a filename (before the extension).
        The suffix is extracted from the config file.
        :param filename: filename to add the suffix to
        :param suffix: suffix given to the compressed file (before the extension)
        :return: filename with suffix appended
        """
        return "{}{}.pdf".format(filename.split(".pdf", 1)[0], suffix)

    @staticmethod
    def __clean_filename(filename):
        """
        Simple way to rename compressed file to the original file name.
        It is not a full proof detection method, but it will hardly present any issue.
        :param filename: file path to adapt
        :return: adapted file path
        """
        return "{}.pdf".format(filename.split("_compress_", 1)[0])

    def __get_files(self, directory, file_extension):
        """
        Get a list of all files of a given type in a directory and optionally its sub-directories.
        :param directory: directory to search
        :param file_extension: file extension to search
        :return: list of found files
        """
        path_spec = "{}**/*.{}" if self.__config.recursive() else "{}*.{}"
        return glob.glob(path_spec.format(directory, file_extension), recursive=self.__config.recursive())

    def __ignore_files_with_suffix(self, files):
        """
        Remove files containing the suffix from list of files to compress.
        :param files: list of files to compress
        :return: new list
        """
        if self.__config.suffix().strip():
            files = [file for file in files if self.__config.suffix() not in file]
        return files

    def __get_files_to_rename(self, directory):
        """
        Get list of recently compressed files to rename.
        :param directory: directory where the compressed files were stored
        :return: files to rename
        """
        return [file for file in self.__get_files(directory, "pdf") if "_compress_" in file]

    def setup(self, option, value):
        """
        Edit user configuration.
        :param option: option to edit
        :param value: new value
        """
        self.__config.update_config(option, value)

    def list_config(self):
        """
        List user configurations.
        """
        self.__config.list_config()

    def valid_configuration(self):
        """
        Check if the configuration is valid.
        :return: True if there is a valid configuration
        """
        valid = True

        if (not self.__config.suffix()) and (self.__config.output_dir() == self.__config.input_dir()):
            print("ERROR: output_dir directory cannot be the same as input_dir with an empty suffix!")
            valid = False
        if not self.__config.public_key():
            print("ERROR: public_key not set! Set it through 'pdfworkshop config public_key <your_key>'. "
                  "A free API key can be obtained from https://developer.ilovepdf.com/")
            valid = False
        return valid

    @staticmethod
    def __percentage_storage_saved(task):
        """
        Calculate the percentage of storage space saved by the compression.
        :param task: information about the task
        :return: percentage of storage space saved
        """
        task_information = task.get_task_information()
        return int((1 - task_information.output_filesize / task_information.filesize) * 100)

    def run(self):
        """
        Run using the stored configurations.
        """
        self.__run(
            self.__config.public_key(),
            self.__config.input_dir(),
            self.__config.output_dir(),
            self.__config.suffix()
        )

    def __run(self, public_key, input_dir, output_dir, suffix):
        """
        Compress PDF files stored in input_dir and store the resultant files in output_dir.
        Authentication is made using the provided public key.
        :param public_key: API development public key
        :param input_dir: directory where the PDF files will be collected from
        :param output_dir: directory where the compressed PDF files will be stored
        :param suffix: the suffix given to the compressed file (before the extension)
        """
        if self.valid_configuration():

            # create directories if they do not exist
            self.__setup_dir(self.__config.input_dir())
            self.__setup_dir(self.__config.output_dir())

            compress = Compress(public_key, verify_ssl=True, proxies=None)
            compress.set_output_folder(output_dir)

            # search input directory for PDFs. Return if there are no matching files
            files = self.__get_files(input_dir, "pdf")
            files = self.__ignore_files_with_suffix(files)
            if not files:
                print("ERROR: there are no files to compressed.")
                return

            [compress.add_file(file) for file in files]

            compress.execute()   # upload files to iLovePDF
            compress.download()  # download resultant file
            print("Compression saved {}% of disk space.".format(
                self.__percentage_storage_saved(compress))
            )
            compress.delete_current_task()

            # unzip response zip, if there is one
            # note that the API response is a zip only if more than one pdf was submitted
            for zip_file in self.__get_files(output_dir, "zip"):
                if "compress_" in zip_file:
                    zip_ref = zipfile.ZipFile(zip_file, 'r')
                    zip_ref.extractall(output_dir)
                    zip_ref.close()
                    os.remove(zip_file)

            # rename all PDFs to their original filename and possibly add a suffix
            [os.rename(filename, self.__rename_file(filename, suffix))
             for filename in self.__get_files_to_rename(output_dir)]
