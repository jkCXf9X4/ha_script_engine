class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        # else:
            # cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]

class Test_sing(metaclass=Singleton):

    def __init__(self, i: int) -> None:
        print("Init")
        self.var = f"unique variable {i}"

class A:
    def __init__(self) -> None:
        self.a = Test_sing(i=2)
        print(self.a.var)

class B:
    def __init__(self) -> None:
        self.b = Test_sing(i=3)
        print(self.b.var)

a = A()

b = B()

print("End")
