import json
import pdb
import logging
from packager.helpers import SpecialChars, DublinCoreXML

class BaseRecord:

    log = None 

    def __init__(self):
        self.log = logging.getLogger("BaseRecord")
        self.data = {}
        self.dc_formatter = None
        self.char_handler = None
        self.project_type = None
        self.construct_methods = None
        self.filename = ""
        self.dirname = ""
        self.permission = ""
        self.email = ""

    def init(self, project_type: str):
        Methods = self.get_project_methods(project_type)
        self.construct_methods = Methods()

        self.dc_formatter = DublinCoreXML()
        self.char_handler = SpecialChars()

    def import_config(self, config_path: str):
        try:
            with open(config_path, 'r') as f:
                configs = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found at {config_path}")
        for key, obj in configs.items():
          self.data[key] = obj

    def set_filename(self, arr: list):
        self.filename = self.construct_methods.construct_filename(self.data, arr)

    def set_dirname(self, arr: list):
        self.dirname = self.construct_methods.construct_dirname(self.data, arr)

    def set_permission(self, arr: list):
        self.permission = self.construct_methods.construct_permission(self.data, arr)

    def set_metadata(self, tsv_string: str):
        arr = tsv_string.split("\t")
        self.set_filename(arr)
        self.set_permission(arr)
        if self.permission == False:
          self.log.warning(f"Cannot publish this record: {self.filename}")
          return None
        self.set_dirname(arr)
        if 'filename' in self.data:
            del self.data['filename']
        if 'permission' in self.data:
            del self.data['permission']
        if 'email' in self.data:
            del self.data['email']
        for key, obj in self.data.items():
            if 'method' in obj.keys():
                method = getattr(self.construct_methods, obj['method'])
                self.data[key]['val'] = method(self, arr, obj['ind'])
            elif 'ind' in obj.keys():
                self.data[key]['val'] = arr[obj['ind']]

    def assemble_properties(self) -> str:
      parts = []
      for key, obj in self.data.items():
          if 'val' in obj.keys():
              method = getattr(self.dc_formatter, key)
              if type(obj['val']) is list:
                   for item in obj['val']:
                       parts.append(method(item))
              else: parts.append(method(obj['val']))
      string = self.dc_formatter.begin_xml()
      string += "".join(part for part in parts if part)
      string += self.dc_formatter.end_xml()
      return string

    def get_project_methods(self, projname):
        """Dynamically imports the methods class from the project's module."""
        try:
            module = __import__(f"packager.{projname}.project_methods", fromlist=['ProjectMethods'])
            return module.ProjectMethods
        except ImportError as e:
            self.log.error(f"Could not import methods for project '{projname}'.")
            raise e

