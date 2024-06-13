import unittest


class TestExceptions(unittest.TestCase):

    def test_try_except(self):
        try:
            # some code here
            pass
        except:
            # handle an exception is any
            pass

        try:
            # some code here
            pass
        except Exception:
            # handle an exception is any
            pass

        try:
            # some code here
            pass
        except Exception as e:
            # handle an exception is any
            pass

    def test_handle_detailed_exception(self):
        try:
            int("home")
        except ValueError:
            print("test_handle_detailed_exception:", "Some ValueError")

        try:
            int("home")
        except ValueError as e:
            print("test_handle_detailed_exception:", e)

        try:
            raise Exception("Exception")
        except ZeroDivisionError as e:
            print("test_handle_detailed_exception:", e)
        except Exception as e:
            print("test_handle_detailed_exception:", e)

    def test_try_except_else(self):
        try:
            pass
        except Exception as e:
            print("test_try_except_else:", e)
        else:
            print("test_try_except_else:", "No exception has occurred")

    def test_try_except_finally(self):
        try:
            int("home")
        except Exception as e:
            print("test_try_except:", "except is working...")
        finally:
            print("test_try_except_finally:", "finally is working...")

        try:
            pass
        except Exception as e:
            print("test_try_except:", "except is working...")
        else:
            print("test_try_except_finally:", "No exception has occurred")
        finally:
            print("test_try_except_finally:", "finally is working...")

    def test_custom_exception(self):
        class CustomException(Exception):
            pass

        try:
            raise CustomException("Custom exception")
        except Exception as e:
            print("test_custom_exception:", e)

        class SecondCustomException(Exception):
            """Exception raised for some errors in the ... .

            Attributes:
                foo -- something which caused the error
                message -- explanation of the error
            """

            def __init__(self, foo, message):
                self.method_to_override = foo
                self.message = message
                super().__init__(self.message)

        try:
            raise SecondCustomException("FOO", "FOO message")
        except Exception as e:
            print("test_custom_exception:", e)


if __name__ == '__main__':
    unittest.main()
