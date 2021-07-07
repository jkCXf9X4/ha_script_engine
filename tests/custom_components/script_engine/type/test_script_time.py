
import unittest
from custom_components.script_engine.type.script_time import ScriptTime

class TestScriptTime(unittest.TestCase):

    def test_at_time(self):
        actual = ScriptTime("12:00")

        required = ScriptTime("12:00")

        self.assertEqual(actual, required)

    def test_add_of_1(self):
        actual = ScriptTime("08:00") + ScriptTime("04:00")

        required = ScriptTime("12:00")

        self.assertEqual(actual, required)

    def test_add_of_2(self):
        actual = ScriptTime("23:00") + ScriptTime("04:00")

        required = ScriptTime("03:00")

        self.assertEqual(actual, required)

    def test_sub_of_1(self):
        actual = ScriptTime("08:00") - ScriptTime("04:00")

        required = ScriptTime("04:00")

        self.assertEqual(actual, required)

    def test_sub_of_2(self):
        actual = ScriptTime("03:00") - ScriptTime("04:00")

        required = ScriptTime("23:00")

        self.assertEqual(actual, required)


if __name__ == '__main__':
    unittest.main()
