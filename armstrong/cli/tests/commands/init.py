import copy
import os
import re
import shutil
import sys

from armstrong.cli.commands.init import init

from .._utils import StubWriter
from .._utils import TestCase


class SecretKeyProperlySet(TestCase):
    def setUp(self):
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = StubWriter
        sys.stderr = StubWriter

        # HACK: need to make sure settings.configure can be
        #       called multiple times
        from django.conf import settings
        settings._wrapped = None

    def tearDown(self):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def assert_secret_key_set(self, name):
        path = os.path.join(os.path.dirname(__file__), name)
        init(path=path)

        with open(os.path.join(path, "settings", "defaults.py")) as f:
            contents = f.read()
            self.assertRegexpMatches(contents, r"SECRET_KEY = '.+'",
                    msg="Should have found a non-empty SECRET_KEY")
        shutil.rmtree(path)

    def test_set_on_standard_project(self):
        self.assert_secret_key_set("test_set_on_standard_project")

    def test_set_on_demo_project(self):
        self.assert_secret_key_set("test_set_on_demo_project")

    def test_set_on_paywal_project(self):
        self.assert_secret_key_set("test_set_on_paywal_project")

    def test_set_on_tutorial_project(self):
        self.assert_secret_key_set("test_set_on_tutorial_project")
