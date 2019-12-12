#!usr/bin/env python3

import pytest
from pdfworkshop import PDFWorkshop


@pytest.mark.manual
class TestApi:

    def test_api_request(self):
        dummy_api_key = "<key>"
        input_dir = "/tmp/pylovepdfapi/input/"
        output_dir = "/tmp/pylovepdfapi/output/"
        suffix = ""

        PDFWorkshop().compress(dummy_api_key, input_dir, output_dir, suffix)
