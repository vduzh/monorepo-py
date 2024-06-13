import unittest


class TestDecorator(unittest.TestCase):

    def test_decorator_as_func(self):
        # declare a decorator
        def log_decorator(func):
            print("log_decorator: func", func)

            def wrapper(args):
                print("log_decorator:wrapper:before")
                print(f"log_decorator:calling func {func} with {args}")
                func(args)
                print("log_decorator:wrapper:after")

            return wrapper

        # apply the decorator to a function
        @log_decorator
        def foo(args):
            print(f"foo function with the argument of {args} is working...")

        # call the decorated function
        foo(100)

        # it is similar to the code below
        foo = log_decorator(foo)
        # foo(100)

    def test_decorator_as_class(self):
        class LogDecorator:

            def __init__(self, func):
                print(f"LogDecorator: func: {func}")
                self.func = func

            def __call__(self, *args, **kwargs):
                print("LogDecorator: before")
                try:
                    return self.func(*args, **kwargs)
                finally:
                    print("LogDecorator: after")

        # apply the decorator to a function
        @LogDecorator
        def foo(args):
            print(f"foo function: with argument {args} called")

        # call the decorated function
        foo(100)

    def test_reuse_decorator(self):
        def validate(f):
            def wrapper(*args):
                if any([arg for arg in args if type(arg) not in (int, float)]):
                    raise ValueError("int or float expected")

                return f(*args)

            return wrapper

        @validate
        def sum_values(*args):
            res = 0
            for arg in args:
                res += arg
            return res

        @validate
        def sub_values(*args):
            (a, *rest) = args
            return a - sum_values(*rest)

        self.assertEqual(12, sum_values(3, 9))
        self.assertEqual(6, sub_values(10, 4))

        with self.assertRaises(ValueError):
            sum_values("3", 9)
        with self.assertRaises(ValueError):
            sub_values("3", 9)

    def test_chaining_decorators(self):
        def foo(f):
            def wrapper(*args, **kwargs):
                print("foo decorator is called with:", args, kwargs)
                return f(*args, **kwargs)

            return wrapper

        def bar(f):
            def wrapper(*args, **kwargs):
                print("bar decorator is called with:", args, kwargs)
                return f(*args, **kwargs)

            return wrapper

        @foo
        @bar
        def test_func(*args, **kwargs):
            print("test_func is called with:", args, kwargs)

        test_func("buzz", bar="bar_value")

    if __name__ == '__main__':
        unittest.main()
