
import unittest
from functools import wraps

class NiceDecorator:
    def __init__(self, *args, **kwargs):
        print("in decorator init")
        print(args)
        print(kwargs)

    def __call__(self, func):
        def my_logic(*args, **kwargs):
            print("in logic")

            print(func)
            print(args)
            print(kwargs)

            self = args[0]
            print(self.test)

            result = func(*args, **kwargs)
            return result
        return my_logic

class TestStringMethods:

    def __init__(self) -> None:
        self.test = "test"

    @NiceDecorator(1, j="2")
    def random_function(self, k, m=4):
        print(f"k:{k}")
        print(f"m:{m}")

    def test_decorator(self):
        self.random_function(3, m=5)

if __name__ == '__main__':
    i = TestStringMethods()
    i.test_decorator()
