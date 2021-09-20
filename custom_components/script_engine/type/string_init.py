

# not used?
class StringInit:
    def __init__(self, item):
        self.item = item

    # def new(self, *args, **kwargs):
    #     new = self.__new__(type(self))
    #     new.__init__(*args, **kwargs)
    #     return new

    def __hash__(self):
        return hash(self.item)

    def __eq__(self, other):
        if not isinstance(other, StringInit):
            return NotImplemented
        return self.item == other.item

    def __ne__(self, other):
        if not isinstance(other, StringInit):
            return NotImplemented
        return self.item != other.item

    def __lt__(self, other):
        if not isinstance(other, StringInit):
            return NotImplemented
        return self.item < other.item

    def __le__(self, other):
        if not isinstance(other, StringInit):
            return NotImplemented
        return self.item <= other.item

    def __gt__(self, other):
        if not isinstance(other, StringInit):
            return NotImplemented
        return self.item > other.item

    def __ge__(self, other):
        if not isinstance(other, StringInit):
            return NotImplemented
        return self.item >= other.item

    def __repr__(self) -> str:
        return self.item.__repr__()

    def __str__(self) -> str:
        return self.item.__str__()

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.item + other.item)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.item - other.item)
        else:
            return NotImplemented

