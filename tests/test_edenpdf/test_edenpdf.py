#!usr/bin/env python3

import os
import pytest
from pdfworkshop import PDFWorkshop
from shutil import copy
import filecmp


def count_files(files_dir):
    return len(files_dir.listdir())


class TestEdenpdf:

    __dummy_file = "dummy_file.pdf"
    __api_key = os.environ['ILOVEPDF_API_TOKEN']

    @staticmethod
    def verify_compression(input_dir, output_dir):
        assert count_files(input_dir) == count_files(output_dir)
        _, res, _ = filecmp.cmpfiles(input_dir, output_dir, input_dir.listdir())
        assert not res

    @staticmethod
    def generate_files(base_file, input_dir, filenames):
        for filename in filenames:
            dummy = input_dir.join(filename)
            copy(base_file, dummy)

    # indirect arg allows values to be obtained through fixture
    @pytest.mark.parametrize(
        "filenames,datadir,tmpdir",
        [
            pytest.param(["dummy_file.pdf"], "", "", id="1file"),
            pytest.param(["dummy_file_1.pdf", "dummy_file_2.pdf"], "", "", id="2files"),
            pytest.param(
                [
                    "1 - Pathfinding - Part1.pdf", "1 - Pathfinding - Part2.pdf", "1 - Pathfinding - Part3.pdf",
                    "1 - Pathfinding - Part4.pdf", "1 - Pathfinding - Part5.pdf",
                ], "", "", id="1zip_3files"
            ),
            pytest.param(
                [
                    "1 - Pathfinding - Part1.pdf", "1 - Pathfinding - Part2.pdf", "1 - Pathfinding - Part3.pdf",
                    "1 - Pathfinding - Part4.pdf", "1 - Pathfinding - Part5.pdf", "1 - Pathfinding - Part6.pdf",
                    "1 - Pathfinding - Part7.pdf",
                ], "", "", id="3zips_1file"
            ),
            pytest.param(
                [
                    "1 - Pathfinding - Part1.pdf", "1 - Pathfinding - Part2.pdf", "1 - Pathfinding - Part3.pdf",
                    "1 - Pathfinding - Part4.pdf", "1 - Pathfinding - Part5.pdf", "1 - Pathfinding - Part6.pdf",
                    "1 - Pathfinding - Part7.pdf", "1 - Pathfinding - Part8.pdf"
                ], "", "", id="4zips"
            ),
        ],
        indirect=["datadir", "tmpdir"]
    )
    def test_light_file_upload(self, datadir, tmpdir, filenames):

        input_dir = tmpdir.mkdir("input")
        output_dir = tmpdir.mkdir("output")
        suffix = ""

        dummy_file = datadir / self.__dummy_file

        self.generate_files(dummy_file, input_dir, filenames)

        PDFWorkshop().compress(self.__api_key, input_dir.strpath + '/', output_dir.strpath + '/', suffix)

        self.verify_compression(input_dir, output_dir)
