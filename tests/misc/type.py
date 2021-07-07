

class test:
    def __init__(self, var) -> None:
        self.var = var

string = "hello"

test_obj = test("bye")
type_test = type(test_obj)

t = type_test(string)

print(t.var)

str(None)