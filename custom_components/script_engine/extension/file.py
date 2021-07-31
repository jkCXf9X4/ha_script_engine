import os

class FileExtension:
    @staticmethod
    def get_folder_from__file__(file):
        full_path = os.path.realpath(file)
        path, filename = os.path.split(full_path)
        return path
