# List of channels you want to translate.
import os
import json


class Filter:
    def __init__(self):
        self.dict_filter = self.__open_json_file__('filter.json')

    def __open_json_file__(self, file_name):
        try:
            dir_name = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(dir_name, file_name)
            with open(path) as f:
                return json.load(f)
        except:
            return None

    def is_allowed(self, name):
        if self.dict_filter is None:
            # all allowed
            return True

        if len(self.dict_filter) == 0:
            # all allowed
            return True

        if self.dict_filter.get(name) is not None:
            return True

        return False
