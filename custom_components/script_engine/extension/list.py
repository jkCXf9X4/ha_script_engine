
from typing import List

class ListExtension:

    @staticmethod
    def split_list(list: List, condition):
        valid = []
        not_valid = []
        for item in list:
            if condition(item):
                valid.append(item)
            else:
                not_valid.append(item)
        return valid, not_valid
