
import os
import fnmatch
import logging
import importlib
import inspect
import re

from typing import List

from custom_components.script_engine.extension.list import ListExtension
from .script_info import ScriptInfo
from .class_info import ClassInfo

class ScriptHandler:
    """
    Locate and instantiate the scripts 
    """

    def __init__(self, path, debug=False) -> None:
        self.path = path
        self.scripts = []
        self.logger = logging.getLogger(__name__)
        self.debug = debug

    def find_files(self, pattern) -> None:
        def init_script(path, file):
            script = ScriptInfo()
            script.path = os.path.join(path, file)
            script.filenmae = file
            script.module_name = file.split(".")[0]
            return script

        scripts: List[ScriptInfo] = [init_script(self.path, name) for name in os.listdir(self.path)]
        self.scripts = [f for f in scripts if fnmatch.fnmatch(f.filenmae, pattern)]

        not self.debug or self.logger.debug(f"Script files: {[i.filenmae for i in self.scripts]}")

    def extract_script_classes(self, pattern):
        def extract_classes(script: ScriptInfo):
            importlib.invalidate_caches()
            module = importlib.import_module(script.module_name)
            members = {i[0]: i[1] for i in inspect.getmembers(module, inspect.isclass)}
            script.class_info_objects = [ClassInfo(_class) for key, _class in members.items() if re.match(pattern, key) != None]

            not self.debug or self.logger.debug(f"Extracted classes:  {[i.script_class_object for i in script.class_info_objects]}")

        _ = [extract_classes(i) for i in self.scripts]

    def instantiate_script_classes(self, *arg, **kwarg):
        def instantiate_classes(scrip_class: ClassInfo):
            scrip_class.script_class = scrip_class.script_class_object(*arg, **kwarg)

            not self.debug or self.logger.debug(f"Created classes:  {scrip_class.script_class}")

        _ = [[instantiate_classes(j) for j in i.class_info_objects] for i in self.scripts]

    def extract_script_functions(self, pattern):

        def is_script_function(func):
            return re.match(pattern, func.__name__) != None

        def extract_functions(scrip_class: ClassInfo):
            attrs = [getattr(scrip_class.script_class, name) for name in dir(scrip_class.script_class) if name[0:2] != "__"]
            functions = [attr for attr in attrs if inspect.ismethod(attr)]
            scrip_class.script_function_objects, scrip_class.non_script_functions_object = ListExtension.split_list(functions, is_script_function)

            not self.debug or self.logger.info(f"\nClass: {scrip_class.script_class_object.__name__} Extracted functions: {' '.join([i.__name__ for i in scrip_class.script_function_objects])}")
            # self.logger.debug(f"Not Extracted: {' '.join([i.__name__ for i in scrip_class.non_script_functions_object])}")

        _ = [[extract_functions(j) for j in i.class_info_objects] for i in self.scripts]

    def instantiate_script_functions(self, *args, **kwargs):
        def instantiate_functions(scrip_class: ClassInfo):
            scrip_class.function_results = [func(*args, **kwargs) for func in scrip_class.script_function_objects]

            not self.debug or self.logger.debug(f"Instantiate status: {scrip_class.function_results}")

        _ = [[instantiate_functions(j) for j in i.class_info_objects] for i in self.scripts]

