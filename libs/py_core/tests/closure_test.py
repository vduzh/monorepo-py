import unittest


class TestClosure(unittest.TestCase):
    def test_closure(self):
        def fn_outer(s: str):
            def fn_inner():
                return s.upper()

            return fn_inner

        fn = fn_outer('home')
        self.assertEqual(fn(), "FOO")
        self.assertEqual(fn(), "FOO")

        self.assertEqual(fn_outer('bar')(), "BAR")

    def test_closure_nonlocal(self):
        def counter(start=0):
            def increase():
                nonlocal start
                start += 1
                return start

            return increase

        counter_1 = counter()
        self.assertEqual(counter_1(), 1)
        self.assertEqual(counter_1(), 2)


if __name__ == '__main__':
    unittest.main()
