

from custom_components.script_engine.decorator.abc.decorator import Decorator
from custom_components.script_engine.decorator.decorator_type import DecoratorType
    
class OrOp(Decorator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = DecoratorType.OPERAND

    def __str__(self) -> str:
        return f"{self.name}:{self.type}:wrap's {self.function.get_name()}"

    def execute(self, *args, **kwargs):
        """Returns new args and kwargs, raise exception if failure to execute"""

        operator_index = self.handler.get_index(self)
        decorators = self.handler.decorators
        result = kwargs["result"]

        def find(dir = 1):
            """ dir: 1 forward, -1 backwards"""
            pos = operator_index
            while (True):
                pos += dir 
                if decorators[pos].type != DecoratorType.BOOLEAN:
                    return pos - dir
                if pos == len(self.handler.decorators) or pos == 0:
                    return pos

        first = find(-1)
        last = find(1)

        pre = all(result[first:operator_index])
        post = all(result[operator_index+1:last+1])

        if pre or post:
            kwargs["result"][first:last+1] = [True] * (last-first)

        return super().execute(*args, **kwargs)
