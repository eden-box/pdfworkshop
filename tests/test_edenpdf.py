#!usr/bin/env python3

import os
import pytest
from pdfworkshop import PDFWorkshop


class TestEdenpdf:

    __api_key = os.environ['ILOVEPDF_API_TOKEN']

    def test_dummy(self):
        assert True
