from .misc import FileHandler

DOMAIN = "script_engine"

FUNCTION_NAME = 'script_'
FILE_NAME_PATTERN = FUNCTION_NAME + '*.py'
FUNCTION_NAME_PATTERN = FUNCTION_NAME + '*'

SCRIPT_FOLDER = "/config/script_engine/"
CUSTOM_COMPONENTS_FOLDER = FileHandler.get_folder_from__file__(__file__)
