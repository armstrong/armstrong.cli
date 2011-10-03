from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from unittest import TestLoader, TestSuite

from . import commands


loader = TestLoader()
suite = TestSuite()
suite.addTests(loader.loadTestsFromModule(commands))
