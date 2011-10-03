from unittest import TestCase
import fudge

StubWriter = fudge.Fake()
StubWriter.provides("write")
