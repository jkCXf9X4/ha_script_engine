import os
import fnmatch 
import logging
import runpy
import inspect
import re

from .engine import Engine

from .misc import ListHelp

class Script_info:
    def __init__(self):
        self.path = None
        self.filenmae = None
        self.module_name = None
        self.class_ = None
        self.class_object = None
        self.functions = None
        self.function_objects = None

class Script_handler:

    def __init__(self, path) -> None:
        self.path = path
        self.scripts = []
        self._LOGGER = logging.getLogger(__name__)

    def find_files(self, pattern) -> None:
        def init_script(path, file):
            script = Script_info()
            script.path = os.path.join(path, file)
            script.filenmae = file
            script.module_name = file.split(".")[0]
            return script

        scripts = [init_script(self.path, name) for name in os.listdir(self.path)]

        self.scripts = [f for f in scripts if fnmatch.fnmatch(f.filenmae, pattern)]

    def extract_script_classes(self):
        def extract_class(script: Script_info):
            glob = globals()
            script_globals = runpy.run_path(path_name=script.path, init_globals=glob)
            script.class_object = script_globals[script.module_name]

        _ = [ extract_class(i) for i in self.scripts]
            
    def instantiate_script_classes(self, *arg, **kwarg):
        def instantiate_class(script: Script_info):
            script._class = script.class_object(*arg, **kwarg)

        _ = [ instantiate_class(i) for i in self.scripts]
           
    def extract_script_functions(self, pattern):
        def extract_function(script: Script_info):
            attrs = [getattr(script._class, name) for name in dir(script._class) if name[0:1] != "_" and re.match(pattern, name) != None]
            script.function_objects = [attr for attr in attrs if inspect.ismethod(attr)]

        _ = [ extract_function(i) for i in self.scripts]

    def instantiate_script_functions(self, *args, **kwargs):
        def instantiate_functions(script: Script_info):
            script.functions = [func(*args, **kwargs) for func in script.function_objects]

        _ = [instantiate_functions(i) for i in self.scripts]

####
# Old stuff 

    # def import_scripts(self):
    #     import importlib
    #     for script in self.scripts:
    #         importlib.import_module(f"{script.module_name}")


    # def create_module_import_index(scripts, path):
    #     with open(os.path.join(path, 'index.py'), 'w') as writer:
    #         for module in scripts:
    #             writer.write(f"from {module} import *\n")
