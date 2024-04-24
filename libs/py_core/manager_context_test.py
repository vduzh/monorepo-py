import unittest


class TestContextManager(unittest.TestCase):
    def test_core(self):
        with open(__file__) as f:
            print(f.name)

    def test_custom_context_manager(self):
        class DefenderVector:
            def __init__(self, v):
                self.__v = v

            def __enter__(self):
                # create a copy to be referenced
                self.__temp = self.__v[:]
                return self.__temp

            def __exit__(self, exc_type, exc_value, exc_traceback):
                if exc_type is None:
                    # there is no any exception
                    # copy data from __temp one by one
                    self.__v[:] = self.__temp

                return False

        # test the correct path
        v1 = [1, 2, 3]
        v2 = [10, 20, 30]

        with DefenderVector(v1) as d:
            for i, a in enumerate(d):
                d[i] += v2[i]

        self.assertEqual([11, 22, 33], v1)

        # test the incorrect path
        v1 = [1, 2, 3]
        v2 = [2, 3]
        try:
            with DefenderVector(v1) as d:
                for i, a in enumerate(d):
                    d[i] += v2[i]
        except IndexError:
            pass

        self.assertEqual([1, 2, 3], v1)


if __name__ == '__main__':
    unittest.main()
