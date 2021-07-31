
import unittest
from datetime import datetime, timedelta

from custom_components.script_engine.type.script_datetime import ScriptDateTime

class TestScriptTime(unittest.TestCase):

    # 2021-07-10T12:42:13.342769+00:00

    def test_at_time(self):
        d = datetime(2020, 3, 4, hour=4, minute=3)

        print(d.isoformat())

        actual = ScriptDateTime("2020-03-04T04:03:00+00:00") 

        required = ScriptDateTime("2020-03-04T04:03:00+00:00")

        self.assertEqual(actual, required)

    def test_add_of_1(self):
        actual = ScriptDateTime("2020-03-04T04:03:00+00:00") + timedelta(days=2, hours=5)

        required = ScriptDateTime("2020-03-06T09:03:00+00:00")

        self.assertEqual(actual, required)

    def test_sub_of_1(self):
        actual = ScriptDateTime("2020-03-04T04:03:00+00:00") - timedelta(days=2, hours=5)

        required = ScriptDateTime("2020-03-01T23:03:00+00:00")

        self.assertEqual(actual, required)

if __name__ == '__main__':
    unittest.main()
