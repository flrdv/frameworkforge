import dataclasses
import unittest

import si


@dataclasses.dataclass
class TestCase:
    string: str
    float: float


class TestSIUnitsOperations(unittest.TestCase):
    def test_parse(self):
        for tc in [
            TestCase("5ns", 5),
            TestCase("5.5ns", 5.5),
            TestCase("5us", 5 * 1000),
            TestCase("5ms", 5 * 1000 * 1000),
            TestCase("5s", 5 * 1000 * 1000 * 1000),
            TestCase("5m", 5 * 1000 * 1000 * 1000 * 60),
        ]:
            value = si.parse(tc.string, qualifiers=si.TIME_QUALIFIERS)
            self.assertEqual(value, tc.float)

    def test_serialize(self):
        for tc in [
            TestCase("5ns", 5),
            TestCase("5.5ns", 5.5),
            TestCase("5us", 5 * 1000),
            TestCase("5ms", 5 * 1000 * 1000),
            TestCase("5s", 5 * 1000 * 1000 * 1000),
            TestCase("5m", 5 * 1000 * 1000 * 1000 * 60),
        ]:
            value = si.serialize(tc.float, qualifiers=si.TIME_QUALIFIERS)
            self.assertEqual(value, tc.string)
