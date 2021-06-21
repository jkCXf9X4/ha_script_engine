import os

from typing import List


class ListHelp:

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


class FileHandler:

    @staticmethod
    def get_folder_from__file__(file):
        full_path = os.path.realpath(file)
        path, filename = os.path.split(full_path)
        return path
