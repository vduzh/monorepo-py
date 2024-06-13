import math
import types
import unittest


# defines a namespace
class SimpleClass:
    """A mock class for test purposes.

    Attributes:
        __private_attr -- the private attribute
        name -- the name if the foo
        description -- the attribute with empty default value
        note -- the attribute with not empty default value
    """

    # attribute or properties
    __private_attr = None

    # attribute or properties
    description = ""

    # attribute or properties
    note = "some note"

    # the constructor of the class
    def __init__(self, name="Buzz"):
        print("SimpleClass",
              f"constructor called with name:{name}, description: {self.description}, __private_attr: {self.__private_attr}", )

        # init name attribute
        self.name = name

    def __str__(self):
        return self.name

    # a method of the class
    def set_name(self, name):
        self.name = name

    def method_of_super_class(self):
        return "SimpleClass"

    def method_to_override(self):
        return "SimpleClass"

    @staticmethod
    def static_method():
        print("I'm a static_method")

    @classmethod
    def class_method(cls):
        print("I'm a class_method")


class TestClasses(unittest.TestCase):
    def test_create_object_from_class(self):
        obj = SimpleClass("Foo")
        obj = SimpleClass("Bar")
        obj = SimpleClass()

    def test_attributes(self):
        # check for attributes
        self.assertTrue(hasattr(SimpleClass, "description"))
        self.assertFalse(hasattr(SimpleClass, "notexist"))

        # read attributes
        attr_value = SimpleClass.note
        self.assertEqual("some note", attr_value)
        attr_value = getattr(SimpleClass, "note")
        self.assertEqual("some note", attr_value)
        attr_value = getattr(SimpleClass, "notexist", None)
        self.assertIsNone(attr_value)

        obj = SimpleClass("Foo")
        # assert the attributes
        self.assertEqual("Foo", obj.name)
        self.assertIsNotNone(obj.set_name)

        class ClassWithoutAttributes:
            pass

        # add attributes to class
        ClassWithoutAttributes.custom_attribute = "bar"

        def custom_method(self_obj): print(f"Custom method is working with {self_obj.custom_attribute}")

        ClassWithoutAttributes.custom_method = custom_method
        self.assertEqual("bar", ClassWithoutAttributes.custom_attribute)

        obj_1 = ClassWithoutAttributes()
        obj_2 = ClassWithoutAttributes()
        self.assertEqual("bar", obj_1.custom_attribute)
        self.assertEqual("bar", obj_2.custom_attribute)

        obj_1.custom_attribute = "home"
        obj_2.custom_attribute = "buzz"
        self.assertEqual("bar", ClassWithoutAttributes.custom_attribute)
        self.assertEqual("home", obj_1.custom_attribute)
        self.assertEqual("buzz", obj_2.custom_attribute)

        obj_1.custom_method()

    def test_add_custom_attribute(self):
        class TestClass:
            pass

        TestClass.foo = "Foo"
        setattr(TestClass, "bar", "Bar")

    def test_delete_attribute(self):
        class TestClass:
            foo = "foo"
            bar = "bar"

        del TestClass.foo
        delattr(TestClass, "bar")

        class Point:
            color = "red"

        p = Point()
        # will be taken from the class namespace
        self.assertEqual("red", p.color)
        p.color = "blue"
        # will be taken from the object namespace
        self.assertEqual("blue", p.color)
        delattr(p, "color")
        # will be taken from the class namespace
        self.assertEqual("red", p.color)

    def test_methods(self):
        # get a ref to the method of the class
        method_ref = SimpleClass.set_name
        self.assertIsInstance(method_ref, types.FunctionType)

        obj = SimpleClass("Foo")
        # get a  ref to the method of an object
        method_ref = obj.set_name
        self.assertIsInstance(method_ref, types.MethodType)

        # call method via object
        obj.set_name("Bar")
        self.assertEqual("Bar", obj.name)

        # call method via the class and the reference to the object
        SimpleClass.set_name(obj, "Buzz")
        self.assertEqual("Buzz", obj.name)

        SimpleClass.class_method()

        SimpleClass.static_method()

    def test_class_methods(self):
        class Data:
            MIN_VALUE = 0

            @classmethod
            def set_min_value(cls, value):
                cls.MIN_VALUE = value

            # regular method
            def foo(self, value):
                self.set_min_value(value)

        d = Data()

        self.assertEqual(0, Data.MIN_VALUE)
        self.assertEqual(0, d.MIN_VALUE)

        d.MIN_VALUE = 5
        self.assertEqual(0, Data.MIN_VALUE)
        self.assertEqual(5, d.MIN_VALUE)

        d.set_min_value(10)
        self.assertEqual(10, Data.MIN_VALUE)
        self.assertEqual(5, d.MIN_VALUE)

    def test_static_methods(self):
        class Util:
            @staticmethod
            def norm2(x, y):
                return x * x + y * y

            # regular method
            def foo(self, x, y):
                return self.norm2(x, y)

        self.assertEqual(500, Util.norm2(10, 20))
        self.assertEqual(109, Util().foo(3, 10))

    def test_properties(self):
        class Data:

            def __init__(self, value, size):
                # init private attributes
                self.__value = value
                self.__size = size

            def get_value(self):
                """Getter for the value property"""
                return self.__value

            def set_value(self, value):
                """Setter for the value property"""
                self.__value = value

            # declare property
            value = property(get_value, set_value)

            @property
            def size(self):
                return self.__size

            @size.setter
            def size(self, s):
                self.__size = s

            @size.deleter
            def size(self):
                del self.__size

        data = Data("foo", 123)

        # test getters and setters
        self.assertEqual("foo", data.get_value())
        data.set_value("bar")
        self.assertEqual("bar", data.get_value())

        # test property
        data.value = "buz"
        self.assertEqual("buz", data.get_value())
        self.assertEqual("buz", data.value)

        self.assertEqual(123, data.size)
        data.size = 200
        self.assertEqual(200, data.size)

        self.assertIsNotNone(data.size)
        del data.size
        self.assertIsNone(getattr(data, "size", None))

    def test_inheritance(self):
        class Parent:  # inherit from object
            name = "Parent"

            def method_of_super_class(self):
                return f"{self.name}::method_of_super_class"

            def method_to_override(self):
                """Simulate the abstract method inheritance"""
                raise NotImplementedError()

            def parent_method(self):
                return f"{self.name}::parent_method:{self.method_to_override()}"

        class Child(Parent):
            name = "Child"

            def method_to_override(self):
                return f"{self.name}::method_to_override"

        class SecondChild(Parent):
            name = "SecondChild"

            def method_to_override(self):
                return f"{self.name}::method_to_override"

        obj = Parent()
        self.assertEqual("Parent", obj.name)
        self.assertEqual("Parent::method_of_super_class", obj.method_of_super_class())
        with self.assertRaises(NotImplementedError):
            obj.method_to_override()
        obj.method_of_super_class()

        obj = Child()
        self.assertEqual("Child", obj.name)
        self.assertEqual("Child::method_to_override", obj.method_to_override())
        self.assertEqual("Child::parent_method:Child::method_to_override", obj.parent_method())
        obj.method_of_super_class()

        obj = SecondChild()
        self.assertEqual("SecondChild", obj.name)
        self.assertEqual("SecondChild::method_to_override", obj.method_to_override())
        self.assertEqual("SecondChild::parent_method:SecondChild::method_to_override", obj.parent_method())
        obj.method_of_super_class()

    def test_multiple_inheritance(self):

        class Left:
            def __init__(self):
                super().__init__()
                print("Left::__init__")

            def foo(self): return "Left::foo is working"

            def buzz(self): return "Left::buzz is working"

        class Right:
            def __init__(self):
                print("Right::__init__")

            def foo(self): return "Right::foo is working"

            def buzz(self): return "Right::buzz is working"

            def bar(self): return "Right::bar is working"

        class SubClass(Left, Right):
            def buzz(self):
                # use buzz from the Right class
                return Right.buzz(self)

        obj = SubClass()
        self.assertEqual("Left::foo is working", obj.foo())
        self.assertEqual("Right::foo is working", Right.foo(obj))
        self.assertEqual("Right::buzz is working", obj.buzz())
        self.assertEqual("Right::bar is working", obj.bar())

        # Mixins
        class MixinLog:
            value = 0

            def __init__(self):
                # tend not to use params
                print("MixinLog::__init__ is working")
                MixinLog.value += 1

            def get_call_count(self):
                return MixinLog.value

        class SubClass(Left, MixinLog):
            pass

        obj = SubClass()
        self.assertEqual(1, obj.get_call_count())
        obj = SubClass()
        self.assertEqual(2, obj.get_call_count())

    def test_inheritance_of_attributes(self):
        class Foo:
            def __init__(self, name, description):
                # private
                self.__name = name
                # protected
                self._description = description

        class Bar(Foo):
            def __init__(self, name, description, size):
                super().__init__(name, description)
                # private
                self.__size = size

            def access_public_and_protected(self):
                print(self._description)

            def access_privates(self):
                print(self.__name)

        bar = Bar("foo", "bar", 100)
        bar.access_public_and_protected()
        with self.assertRaises(AttributeError):
            bar.access_privates()

    def test_super(self):
        class Foo:
            def __init__(self, name):
                self.name = name

        class Bar(Foo):
            def __init__(self, name, size):
                # call the initializer of the parent class
                super().__init__(name)
                self.size = size

        foo = Foo("foo")
        bar = Bar("bar", 100)

    def test_issubclass(self):
        class Foo:
            pass

        class Bar(Foo):
            pass

        self.assertTrue(issubclass(Foo, object))
        self.assertTrue(issubclass(Bar, Foo))

    def test_inner_types_are_objects(self):
        self.assertTrue(issubclass(int, object))
        self.assertTrue(issubclass(float, object))
        self.assertTrue(issubclass(bool, object))

    def test_isinstance(self):
        class Foo:
            pass

        foo = Foo()

        self.assertTrue(isinstance(foo, object))
        self.assertTrue(isinstance(foo, Foo))

    def test_encapsulation(self):
        class Point:

            def __init__(self, x, y, z):
                # public
                self.x = x
                # protected
                self._y = y
                # private
                self.__validate(z)
                self.__z = z

            @property
            def z(self): return self.__z

            @z.setter
            def z(self, value):
                self.__validate(value)
                self.__z = value

            @staticmethod
            def __validate(value):
                # private method
                if type(value) not in (int, float):
                    raise ValueError(f"Invalid value {value}. Expected int or float")

        p = Point(1, 5, 10)
        p.z = 100
        with self.assertRaises(ValueError):
            p.z = "100"

        # NOTE: Note recommended!!!
        p._Point__z = 200
        self.assertEqual(200, p.z)

    def test_polymorphism(self):
        """Work with different objects via the same interface"""

        # without inheritance
        class Foo:
            def sayHello(self):
                pass

        class Bar:
            def sayHello(self):
                pass

        lst = [Foo(), Bar()]
        for obj in lst:
            obj.sayHello()

        # without inheritance
        class Base:
            def sayHello(self):
                """Simulate an abstract method"""
                raise NotImplementedError()

        class Foo(Base):
            def sayHello(self):
                pass

        class Bar(Base):
            def sayHello(self):
                pass

        lst = [Foo(), Bar()]
        for obj in lst:
            obj.sayHello()

    def test_descriptors(self):
        class CoordinateDescriptor:
            def __set_name__(self, owner, name):
                self.name = "_" + name

            def __get__(self, instance, owner):
                # return instance.__dict__[self.name]
                return getattr(instance, self.name)

            def __set__(self, instance, value):
                print(f"__set__: {self.name} = {value}")
                # put validation code here
                self.__validate(value)
                # instance.__dict__[self.name] = value
                setattr(instance, self.name, value)

            @staticmethod
            def __validate(value):
                if type(value) not in (int, float):
                    raise ValueError(f"Invalid value {value}. Expected int or float")

        class Point:
            x = CoordinateDescriptor()
            y = CoordinateDescriptor()

            def __init__(self, x, y):
                self.x = x
                self.y = y

        point = Point(1, 2)
        print(point.__dict__)
        self.assertEqual(1, point.x)

        with self.assertRaises(ValueError):
            Point("1", 2)

    def test__attributes__(self):
        class_attribute_dict = SimpleClass.__dict__
        # pprint(attribute_dict)
        self.assertIsNotNone(class_attribute_dict["description"])

        obj = SimpleClass("Foo")
        obj_attribute_dict = obj.__dict__
        self.assertEqual({'name': 'Foo'}, obj_attribute_dict)
        obj.description = "test description"
        self.assertEqual({'name': 'Foo', 'description': 'test description'}, obj_attribute_dict)

        class Foo:
            pass

        foo = Foo()

        self.assertEqual("Foo", Foo.__name__)
        self.assertEqual(Foo, foo.__class__)
        self.assertEqual((Foo, object), Foo.__mro__)

    def test__new__(self):
        # gets called before an object creation

        class Point:
            def __new__(cls, *args, **kwargs):
                """Create a Point object.

                :param args: (x, y)
                :param kwargs: {}
                """
                print(f"__new__ for class {cls} with args {args} and kwargs {kwargs}")
                # create an instance of the class
                return super().__new__(cls)

            def __init__(self, x, y):
                print(f"__init__ object {self}  with y={x} and y={y}")
                self.x = x
                self.y = y

        p = Point(1, 9)

        # Singleton
        class Singleton:
            # keep a single instance of the class
            __instances = None

            def __new__(cls, *args, **kwargs):
                if cls.__instances is None:
                    cls.__instances = super().__new__(cls)
                return cls.__instances

            def __del__(self):
                Singleton.__instances = None

            # TODO: call must be implemented

        s1 = Singleton()
        s2 = Singleton()

        self.assertEqual(id(s1), id(s2))

    def test__init__(self):
        class Point:
            # initialize an object of the class
            def __init__(self, x, y):
                super().__init__()
                print(f"__init__ called with y={x} and y={y}")
                self.x = x
                self.y = y

        p = Point(1, 9)
        self.assertEqual({'x': 1, 'y': 9}, p.__dict__)

    def test__del__(self):
        class Point:

            # finalize the object
            def __del__(self):
                print(f"__del__ called for the obj: {self}")

        p = Point()

    def test__call__(self):
        class Counter:
            """Functor class as it has the __call__ method"""

            def __new__(cls, *args, **kwargs):
                print(f"__new__ called with args {args} and kwargs {kwargs}")
                return super().__new__(cls)

            def __init__(self, value):
                print(f"__init__ called with value: {value}")
                self.value = value

            def __call__(self, step=1, *args, **kwargs):
                print(f"__call__ called with args: {args} and kwargs: {kwargs}")
                self.value += step
                return self.value

        obj = Counter(100)
        obj(3)
        obj(2)
        res = obj(5)
        self.assertEqual(110, res)

        class Derivative:
            def __init__(self, func):
                self.__func = func

            def __call__(self, x, dx=0.000001, *args, **kwargs):
                return (self.__func(x + dx) - self.__func(x)) / dx

        derivative = Derivative(lambda x: x * x)
        print(derivative(10))
        derivative = Derivative(lambda x: math.sin(x))
        print(derivative(math.pi / 2))

        # use class as decorator
        @Derivative
        def some_func(x): return x * x

        print(some_func(10))

    def test__getattribute__(self):
        class Point:
            x = 100

            def __getattribute__(self, name):
                print(f"__getattribute__ called for the obj: {self} and name: {name} ")

                # add some custom behaviour
                if name != "x":
                    raise ValueError(f"access to {name} attribute denied")

                return object.__getattribute__(self, name)

        p = Point()

        self.assertEqual(100, p.x)
        with self.assertRaises(ValueError):
            print(p.y)

    def test__setattr__(self):
        class Point:

            def __init__(self, x):
                self.x = x

            def __setattr__(self, key, value):
                print(f"__setattr__ called for the obj: {self}, key: {key} and value: {value}")

                # add some custom behaviour
                if key != "x":
                    raise ValueError(f"access to {key} attribute denied")

                return object.__setattr__(self, key, value)

        p = Point(100)
        with self.assertRaises(ValueError):
            p.y = 5

    def test__getattr__(self):
        class Point:

            def __getattr__(self, item):
                print(f"__getattr__ called for the obj: {self} and name: {item} ")
                return False

        p = Point()
        self.assertFalse(p.foo)

        class Data:

            def __getattr__(self, item):
                return object.__getattr__(self, item)

        d = Data()
        with self.assertRaises(AttributeError):
            d.foo

    def test__delattr__(self):
        class Point:

            def __init__(self, x):
                self.x = x

            def __delattr__(self, item):
                print(f"__delattr__ called for the obj: {self} and name: {item} ")
                object.__delattr__(self, item)

        p = Point(100)
        self.assertTrue(hasattr(p, 'x'))
        # print(p.__dict__)
        del p.x
        self.assertFalse(hasattr(p, 'x'))
        # print(p.__dict__)

    def test__str__(self):
        # object info for users
        class User:

            def __init__(self, login):
                self.__login = login

            def __str__(self):
                return f"login: {self.__login}"

        user = User("foo")
        self.assertEqual("login: foo", str(user))
        print(user)

    def test__repr__(self):
        # object info for debugging
        class User:

            def __init__(self, login):
                self.__login = login

            def __repr__(self):
                return f"{self.__class__}: {self.__login}"

        user = User("foo")
        print(repr(user))

    def test__len__(self):
        # object info for users
        class Point:

            def __init__(self, *args):
                self.__coordinates = args

            def __len__(self):
                return len(self.__coordinates)

        point = Point(1, 20, 0)
        self.assertEqual(3, len(point))

    def test__abs__(self):
        # object info for users
        class Point:

            def __init__(self, x):
                self.__x = x

            def __abs__(self):
                return abs(self.__x)

        point = Point(-20)
        self.assertEqual(20, abs(point))

    def test__add__(self):
        class MyInteger:
            def __init__(self, value: int = 0):
                self.data = value

            def __add__(self, other):
                value = 0
                if isinstance(other, MyInteger):
                    value = other.data
                else:
                    value = other

                return MyInteger(self.data + value)

        res = MyInteger(5) + 70
        self.assertEqual(75, res.data)

        res = MyInteger(5) + MyInteger(70)
        self.assertEqual(75, res.data)

    def test__sub__(self):
        class MyInteger:
            def __init__(self, value: int = 0):
                self.data = value

            def __sub__(self, other):
                value = 0
                if isinstance(other, MyInteger):
                    value = other.data
                else:
                    value = other

                return MyInteger(self.data - value)

        res = MyInteger(80) - 75
        self.assertEqual(5, res.data)

        res = MyInteger(80) - MyInteger(75)
        self.assertEqual(5, res.data)

    def test__mul__(self):
        class MyInteger:
            def __init__(self, value: int = 1):
                self.data = value

            def __mul__(self, other):
                value = 1
                if isinstance(other, MyInteger):
                    value = other.data
                else:
                    value = other

                return MyInteger(self.data * value)

        res = MyInteger(10) * 5
        self.assertEqual(50, res.data)

        res = MyInteger(80) * MyInteger(10)
        self.assertEqual(800, res.data)

    def test__truediv__(self):
        class MyInteger:
            def __init__(self, value: int = 1):
                self.data = value

            def __truediv__(self, other):
                value = 1
                if isinstance(other, MyInteger):
                    value = other.data
                else:
                    value = other

                return MyInteger(self.data / value)

        res = MyInteger(10) / 5
        self.assertEqual(2, res.data)

        res = MyInteger(80) / MyInteger(10)
        self.assertEqual(8, res.data)

    def test__or__(self):
        class Pipeable:
            def __init__(self, value=""): self.data = value

            def __or__(self, other):
                return Pipeable(self.data + " " + other.data)

        res = Pipeable("Hello") | Pipeable("World") | Pipeable("!")
        self.assertEqual("Hello World !", res.data)

    def test__eq__(self):
        class MyInteger:
            def __init__(self, value: int = 0): self.data = value

            def __eq__(self, other): return self.data == other.data

        self.assertEqual(MyInteger(10), MyInteger(10))

    def test__ne__(self):
        class MyInteger:
            def __init__(self, value: int = 0): self.data = value

            def __ne__(self, other): return self.data != other.data

        self.assertNotEqual(MyInteger(10), MyInteger(20))

    def test__lt__(self):
        class MyInteger:
            def __init__(self, value: int = 0): self.data = value

            def __lt__(self, other): return self.data < other.data

        self.assertTrue(MyInteger(10) < MyInteger(20))

    def test__le__(self):
        class MyInteger:
            def __init__(self, value: int = 0): self.data = value

            def __le__(self, other): return self.data <= other.data

        self.assertTrue(MyInteger(10) <= MyInteger(20))
        self.assertTrue(MyInteger(10) <= MyInteger(10))

    def test__gt__(self):
        class MyInteger:
            def __init__(self, value: int = 0): self.data = value

            def __gt__(self, other): return self.data > other.data

        self.assertTrue(MyInteger(10) > MyInteger(5))

    def test__ge__(self):
        class MyInteger:
            def __init__(self, value: int = 0): self.data = value

            def __ge__(self, other): return self.data >= other.data

        self.assertTrue(MyInteger(10) >= MyInteger(5))
        self.assertTrue(MyInteger(10) >= MyInteger(10))

    def test__eq__(self):
        class Point:

            def __init__(self, x): self.x = x

        p1 = Point(1)
        p2 = Point(1)

        self.assertFalse(p1 == p2)

        class Data:

            def __init__(self, value): self.value = value

            def __eq__(self, other): return self.value == other.value

        d1 = Data(1)
        d2 = Data(1)

        self.assertTrue(d1 == d2)

    def test__hash__(self):
        class Data:

            def __init__(self, value): self.value = value

            def __eq__(self, other): return self.value == other.value

        d1 = Data(1)
        d2 = Data(1)

        self.assertTrue(d1 == d2)
        with self.assertRaises(TypeError):
            # unhashable type error
            res = hash(d1) == hash(d2)

        class Container:

            def __init__(self, value, weight):
                self.value = value
                self.weight = weight

            def __eq__(self, other):
                return self.value == other.value and self.weight == other.weight

            def __hash__(self):
                return hash((self.value, self.weight))

        c1 = Container(1, 10)
        c2 = Container(1, 10)

        self.assertTrue(c1 == c2)
        self.assertTrue(hash(c1) == hash(c2))

    def test__bool__(self):
        class Point:

            def __init__(self, x): self.x = x

        p = Point(1)
        self.assertTrue(bool(p))

        class PointWithLen(Point):

            def __len__(self): return self.x

        self.assertTrue(bool(PointWithLen(1)))
        self.assertFalse(bool(PointWithLen(0)))

        class PointWithBool(Point):

            def __bool__(self): return self.x != 0

        self.assertTrue(bool(PointWithBool(1)))
        self.assertFalse(bool(PointWithBool(0)))

    def test__getitem__(self):
        class Student:
            def __init__(self, name, marks):
                self.name = name
                self.marks = marks

            def __getitem__(self, key):
                return self.marks[key]

        student = Student("John", [5, 4, 2, 3, 3, 5])
        self.assertTrue(4, student[1])

    def test__setitem__(self):
        class Student:
            def __init__(self, name, marks):
                self.name = name
                self.marks = marks

            def __setitem__(self, key, value):
                if key >= len(self.marks):
                    # extend the marks list
                    off = key + 1 - len(self.marks)
                    self.marks.extend([None] * off)

                self.marks[key] = value

        student = Student("John", [5, 4, 2, 3, 3, 5])
        student[1] = 5
        student[10] = 2
        self.assertTrue(1, student.marks[5])
        self.assertTrue(2, student.marks[10])

    def test__delitem__(self):
        class Student:
            def __init__(self, name, marks):
                self.name = name
                self.marks = marks

            def __delitem__(self, key):
                del self.marks[key]

        student = Student("John", [5, 4, 2, 3, 3, 5])
        del student[1]
        self.assertTrue([5, 2, 3, 3, 5], student.marks)

    def test__next__(self):
        class MyRange:
            def __init__(self, start=0, stop=10, step=1):
                self.start = start
                self.stop = stop
                self.step = step

                # NOTE: Interesting approach!
                self.value = self.start - self.step

            def __next__(self):
                if self.value + self.step > self.stop:
                    raise StopIteration

                self.value = self.value + self.step
                return self.value

        my_range = MyRange(0, 2, 1)

        # my_range is iterator now - we can use next now
        self.assertEqual(0, next(my_range))
        self.assertEqual(1, next(my_range))
        self.assertEqual(2, next(my_range))
        with self.assertRaises(StopIteration):
            next(my_range)

    def test__iter__(self):
        class MyRange:
            def __init__(self, start=0, stop=10, step=1):
                self.start = start
                self.stop = stop
                self.step = step

            def __iter__(self):
                self.value = self.start - self.step
                return self

            def __next__(self):
                if self.value + self.step > self.stop:
                    raise StopIteration

                self.value = self.value + self.step
                return self.value

        my_range = MyRange(0, 2, 1)
        for i in my_range:
            print(i)

    def test__doc__(self):
        doc = SimpleClass.__doc__
        print("test__doc__:", doc)

    def test__slots__(self):
        class Foo:
            # applied to local attributes only
            __slots__ = ("name", "age")

            MAX_VALUE = 100

            def __init__(self, name, age):
                self.name = name
                self.age = age

        foo = Foo("foo", 10)
        self.assertEqual("foo", foo.name)
        self.assertEqual(10, foo.age)

        with self.assertRaises(AttributeError):
            # there is no __dict__ any longer
            d = foo.__dict__

        with self.assertRaises(AttributeError):
            foo.buzz = 100

        self.assertEqual(100, foo.MAX_VALUE)

        # test properties
        class Foo:
            __slots__ = "__name",

            def __init__(self, name):
                self.__name = name

            @property
            def name(self):
                return self.__name

            @name.setter
            def name(self, value):
                self.__name = value

        foo = Foo("foo")
        self.assertEqual("foo", foo.name)

        # test inheritance
        class Foo:
            __slots__ = "name",

            def __init__(self, name):
                self.name = name

        # without __slots__
        class Bar(Foo):
            pass

        bar = Bar("foo")
        bar.age = 100

        # with __slots__
        class Bar(Foo):
            __slots__ = "age",

            def __init__(self, name, age):
                super().__init__(name)
                self.age = age

        bar = Bar("foo", 100)
        with self.assertRaises(AttributeError):
            bar.buzz = 5

    def test__sizeof__(self):
        class Foo:
            def __init__(self):
                self.value = 100

        obj = Foo()
        print(obj.__sizeof__() + obj.__dict__.__sizeof__())


if __name__ == '__main__':
    unittest.main()
