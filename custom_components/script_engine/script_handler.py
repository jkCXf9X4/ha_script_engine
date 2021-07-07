
import os
import fnmatch
import logging
import importlib
import inspect
import re

from .misc import ListHelp

class ClassInfo:
    def __init__(self, obj):
        self.script_class_object = obj
        self.script_class = None
        self.script_function_objects = None
        self.script_functions = None
        self.non_script_functions_object = None
        self.non_script_functions = None

class ScriptInfo:
    def __init__(self):
        self.path = None
        self.filenmae = None
        self.module_name = None
        self.class_info_objects = None

class ScriptHandler:

    def __init__(self, path) -> None:
        self.path = path
        self.scripts = []
        self.logger = logging.getLogger(__name__)

    def find_files(self, pattern) -> None:
        def init_script(path, file):
            script = ScriptInfo()
            script.path = os.path.join(path, file)
            script.filenmae = file
            script.module_name = file.split(".")[0]
            return script

        scripts = [init_script(self.path, name) for name in os.listdir(self.path)]

        self.scripts = [f for f in scripts if fnmatch.fnmatch(f.filenmae, pattern)]

    def extract_script_classes(self, pattern):
        def extract_classes(script: ScriptInfo):
            module = importlib.import_module(script.module_name)
            members = {i[0]: i[1] for i in inspect.getmembers(module, inspect.isclass)}
            script.class_info_objects = [ClassInfo(_class) for key, _class in members.items() if re.match(pattern, key) != None]

            self.logger.debug(f"Extracted classes:  {[i.script_class_object for i in script.class_info_objects]}")

        _ = [extract_classes(i) for i in self.scripts]

    def instantiate_script_classes(self, *arg, **kwarg):
        def instantiate_classes(scrip_class: ClassInfo):
            scrip_class.script_class = scrip_class.script_class_object(*arg, **kwarg)

            self.logger.debug(f"Created classes:  {scrip_class.script_class}")

        _ = [[instantiate_classes(j) for j in i.class_info_objects] for i in self.scripts]

    def extract_script_functions(self, pattern):

        def is_script_function(func):
            return re.match(pattern, func.__name__) != None

        def extract_functions(scrip_class: ClassInfo):
            attrs = [getattr(scrip_class.script_class, name) for name in dir(scrip_class.script_class) if name[0:2] != "__"]
            functions = [attr for attr in attrs if inspect.ismethod(attr)]
            scrip_class.script_function_objects, scrip_class.non_script_functions_object = ListHelp.split_list(functions, is_script_function)

            self.logger.debug(f"Class: {scrip_class.script_class_object.__name__}")
            self.logger.debug(f"Extracted functions: {' '.join([i.__name__ for i in scrip_class.script_function_objects])}")
            self.logger.debug(f"Not Extracted: {' '.join([i.__name__ for i in scrip_class.non_script_functions_object])}")

        _ = [[extract_functions(j) for j in i.class_info_objects] for i in self.scripts]

    def instantiate_script_functions(self, *args, **kwargs):
        def instantiate_functions(scrip_class: ClassInfo):
            scrip_class.function_results = [func(*args, **kwargs) for func in scrip_class.script_function_objects]

            self.logger.debug(f"Instantiate status: {scrip_class.function_results}")

        _ = [[instantiate_functions(j) for j in i.class_info_objects] for i in self.scripts]

