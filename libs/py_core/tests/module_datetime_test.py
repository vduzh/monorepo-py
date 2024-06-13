import datetime as dt
import unittest


class TestDateTime(unittest.TestCase):
    def test_today(self):
        date = dt.date.today()
        print(date)

    def test_time(self):
        time = dt.time(10, 30, 45)
        print(time)

    def test_datetime(self):
        date_time = dt.datetime.now()
        date_time = dt.datetime(year=2022, month=3, day=10, hour=6, minute=23, second=15)
        self.assertEqual(date_time.year, 2022)
        self.assertEqual(date_time.month, 3)
        self.assertEqual(date_time.day, 10)
        self.assertEqual(date_time.time(), dt.time(6, 23, 15))

        print(date_time)

    def test_replace(self):
        date_time = dt.datetime.now()
        date_time = date_time.replace(year=2022)
        self.assertEqual(date_time.year, 2022)

    def test_compare(self):
        dt1 = dt.datetime(2022, 6, 1, 12)
        dt2 = dt.datetime(2022, 1, 6, 12)
        self.assertTrue(dt1 > dt2)
        self.assertTrue(dt2 < dt2)

    def test_delta(self):
        dt1 = dt.datetime(2022, 6, 1, 12)
        dt2 = dt.datetime(2022, 1, 6, 12)
        time_delta = dt1 - dt2
        self.assertEqual(time_delta.days, 146)

        dt1 = dt.datetime(2022, 6, 1)
        time_delta = dt.timedelta(days=2)
        self.assertEqual(dt1 + time_delta, dt.datetime(2022, 6, 3))


    if __name__ == '__main__':
        unittest.main()
