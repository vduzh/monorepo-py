import random
import types
import unittest
from inspect import isfunction

some_global_var = "Foo"


class TestFunctions(unittest.TestCase):
    def test_create_func(self):
        def some_func():
            pass

        # some_func is a name that store the function object like: some_func = () -> pass

    def test_create_func_with_local_var(self):
        def some_func():
            some_local_var = "home"
            return some_local_var

        with self.assertRaises(NameError) as context:
            some_local_var
        self.assertTrue('is not defined' in context.exception.args[0])

    def test_call_func(self):
        def some_func(): print("test_call_func")

        another_ref = some_func

        some_func()
        another_ref()

    def test_check_is_function(self):
        def subtract(a, b): return a - b

        self.assertTrue(hasattr(subtract, "__call__"))
        self.assertTrue(callable(subtract))

        self.assertTrue(isinstance(subtract, types.FunctionType))
        self.assertTrue(isfunction(subtract))

        # self.assertTrue(type(subtract) == function)

    def test_def_is_operation(self):

        if random.random() <= 0.5:
            def some_func():
                return True
        else:
            def some_func():
                return False

        print(some_func())

    def test_empty_func(self):
        def empty_func(): pass

        empty_func()

    def test_func_with_arguments(self):
        def func_with_arguments(data, value): print('param:', data, value)

        # pass arguments by position
        func_with_arguments("Hello", "World!")
        # pass arguments by name
        func_with_arguments(value="World!", data="Hello")

        # argument as tuple
        def func_with_args(*args): print('args param', type(args), args, sep=": ")

        func_with_args("Hello", "World!")

        # argument as dict
        def func_with_kwargs(**kwargs): print('kwargs param', type(kwargs), kwargs, sep=": ")

        func_with_kwargs(start="Hello", end="World!")

        # 2 arguments: tuple and dict
        def func_with_args_and_kwargs(*args, **kwargs):
            print('both args and kwargs params:', type(args), args, type(kwargs), kwargs, sep=", ")

        func_with_args_and_kwargs("foo", "bar", start="Hello", end="World!")

        def func_name_and_rest(foo, *args): print(f"name and rest: {foo}, {args}")

        func_name_and_rest(100, "Hello", "World!")

        def func_name_and_rest_2(*args, foo): print(f"name and rest 2: {args}, {foo}")

        func_name_and_rest_2("Hello", "World!", foo=100)

        def func_name_and_rest_3(*args, foo="Foo"): print(f"name and rest 3: {args}, {foo}")

        func_name_and_rest_3("Hello", "World!")

        def func_with_mix(foo, bar, *args, **kwargs): print(f"all types of arguments: {foo}, {bar}, {args}, {kwargs}")

        func_with_mix(
            100,
            2.1,
            # positional unlimited arguments
            "Hello", "World!",
            # dictionary unlimited arguments
            greeting="Hi!"
        )

    def test_func_as_arguments(self):
        def func1(foo): print(f"func1: {foo}")

        def func2(bar, size): print(f"func2: {bar} and {size}")

        def exec_func(*args):
            func, *params = args
            func(*params)

        exec_func(func1, "Foo")
        exec_func(func2, "Bar", 123)

    def test_unpack_arguments(self):
        # just a simple function
        def func(a, b): print(f"test_unpack_arguments: {a}, {b}")

        func(1, 2)

        # unpack tuple
        test_tuple = (10, 20)
        func(*test_tuple)

        # unpack dict
        test_dict = {"a": 100, "b": 200}
        func(**test_dict)

    def test_polymorphism(self):
        def times(x, y): return x * y

        self.assertEqual(6, times(2, 3))
        self.assertEqual("===", times("=", 3))
        self.assertRaises(TypeError, lambda x: times(times, 3))

    def test_return_value_func(self):
        def return_value_func(): return 1

        def return_multy_value_func(): return 1, 2

        def return_none_value_func(): pass

        self.assertEqual(1, return_value_func())
        # tuple
        self.assertEqual((1, 2), return_multy_value_func())
        self.assertEqual(None, return_none_value_func())

    def test_with_def_value(self):
        def with_def_value(name="John"): return "Hello " + name

        self.assertEqual(with_def_value("Mike"), "Hello Mike")
        self.assertEqual(with_def_value(), "Hello John")

    def test_params_with_types(self):
        def params_with_types(a: int | float, b: int | float) -> int | float: return a + b

        self.assertEqual(params_with_types(1, 2), 3)
        self.assertEqual(params_with_types(1.5, 2.5), 4.0)

    def test_lambda(self):
        self.assertEqual((lambda x, y: x + y)(1, 2), 3)

    def test_yield(self):
        raise NotImplementedError()

    def test_global(self):
        def some_func():
            global some_global_var
            some_global_var = "home"

        some_func()

        self.assertEqual("home", some_global_var)

    def test_nonlocal(self):
        some_nonlocal_var = "Bar"

        def some_func():
            nonlocal some_nonlocal_var
            some_nonlocal_var = "bar"

        some_func()

        self.assertEqual("bar", some_nonlocal_var)

    def test_closures(self):
        def maker(n):
            maker_var = n * 10

            def action(x):
                return maker_var + x

            return action

        first_action_func = maker(2)
        self.assertIsInstance(first_action_func, types.FunctionType)
        self.assertEqual(25, first_action_func(5))

        second_action_func = maker(5)
        self.assertIsInstance(second_action_func, types.FunctionType)
        self.assertEqual(51, second_action_func(1))

    def test_attributes(self):
        # fn_name = sys._getframe().f_code.co_name
        # print(fn_name)
        raise NotImplementedError()

    def test_assign_attributes(self):
        def some_func(): pass

        some_func.attr = "home"

        print(some_func)


if __name__ == '__main__':
    unittest.main()
