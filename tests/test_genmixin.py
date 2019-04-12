#!/usr/bin/env python
import unittest

from genmixin import ReprMixin, EqualityMixin


class MyEmptyReprClass(ReprMixin):
    pass


class MyReprClass(ReprMixin):
    name: str = None
    age: int = None
    spouse: 'MyReprClass' = None
    ReprMixin.repr_add_attr('name age spouse'.split())
    ReprMixin.repr_ignore_empty_attrs()

    def __init__(self, name: str, age: int = None,
                 spouse: 'MyReprClass' = None) -> None:
        self.name = name
        self.age = age
        self.spouse = spouse


class TestReprMixin(unittest.TestCase):
    def test_repr_defaults(self):
        myobj = MyEmptyReprClass()
        self.assertTrue(hasattr(myobj, "_attrs_filter"))
        self.assertTrue(hasattr(myobj, "_attrs_ignore_empty"))

    def test_repr_obj_init(self):
        fred = MyReprClass('Fred', 43)
        self.assertEqual(len(fred._attrs_filter), 3)

        # fred should be valid code
        fred_src = f"{fred!r}"
        print(f"fred_src={fred_src}")
        compile(fred_src, 'fred object', 'eval')

    def test_repr_body(self):
        fred = MyReprClass('Fred', 43)
        fred_evaled = eval(f"{fred!r}")
        fred_expected = "MyReprClass(name='Fred', age=43)"
        self.assertEqual(fred_expected, f"{fred!r}")
        self.assertEqual(fred_expected, f"{fred_evaled!r}")


class MyEqualityClassFrank(EqualityMixin):
    class_field: int = None  # None value gets not compared
    _attrs_ignore_empty = True

    def __init__(self, name: str, age: int = None):
        self.name = name
        self.age = age
        self.salary = None
        EqualityMixin.__init__(self)

    def get_name(self):
        return self.name


class MyEqualityClassJoe(EqualityMixin):
    name = "Joe"
    age = 61

    def __init__(self, name: str = None, age: int = None):
        if name:
            self.name = name
        if age:
            self.age = age
        EqualityMixin.__init__(self)


class TestEqualityMixin(unittest.TestCase):
    def setUp(self):
        self.frank = MyEqualityClassFrank('Frank', 29)
        self.joe = MyEqualityClassJoe()

    def test_eq_init(self):
        self.assertEqual(self.frank._compare_fields, 'name age'.split())
        self.assertEqual(self.joe._compare_fields, 'name age'.split())

    def test_eq(self):
        self.assertEqual(self.frank, MyEqualityClassFrank('Frank', 29))
        self.assertEqual(self.frank, MyEqualityClassFrank('Frank'))
        self.assertNotEqual(self.frank, MyEqualityClassFrank('Frankie'))
        self.assertNotEqual(self.frank, MyEqualityClassFrank('Frankie', 29))

        # None and empty are defaulted to Joe and 61
        self.assertEqual(self.joe, MyEqualityClassJoe())
        self.assertEqual(self.joe, MyEqualityClassJoe('Joe'))
        self.assertEqual(self.joe, MyEqualityClassJoe('Joe', 61))
        self.assertEqual(self.joe, MyEqualityClassJoe(age=61))
        self.assertEqual(self.joe, MyEqualityClassJoe(name='', age=61))
        self.assertNotEqual(self.joe, MyEqualityClassJoe(name='Fred', age=61))
