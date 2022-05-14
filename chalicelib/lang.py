# emoji-flag to ISO 639-1 language code.
# see also:
#  - https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
#  - https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
#  - https://emojipedia.org/flags/
#  - https://wikitravel.org/en/Main_Page
#  - https://cloud.google.com/translate/docs/languages?hl=en
#  - https://tech.yandex.com/translate/doc/dg/concepts/api-overview-docpage/
#  - https://msdn.microsoft.com/en-us/library/hh456380.aspx
import os
import json


class Lang:
    def __init__(self):
        self.dict_flag = self.__open_json_file__('lang_flag.json')
        self.dict_google = self.__open_json_file__('lang_google.json')
        self.dict_ms = self.__open_json_file__('lang_ms.json')
        self.dict_yandex = self.__open_json_file__('lang_yandex.json')
        self.dict_deepl = self.__open_json_file__('lang_deepl.json')

    def __open_json_file__(self, file_name):
        try:
            dir_name = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(dir_name, file_name)
            with open(path) as f:
                return json.load(f)
        except:
            return None

    def __print_list_diff__(self, ln):
        if self.dict_flag is None:
            print('dict_flag is None')
            return

        if ln is None:
            print('input list is None')
            return

        for item in set(self.dict_flag.values()):
            if item not in ln:
                print('{} is not found in flag list.'.format(item))

    def get_lang(self, flag):
        if self.dict_flag is None:
            return None

        name = self.dict_flag.get(flag)
        if name is None or name == "":
            return None
        return name

    def get_google(self, lang):
        if self.dict_google is None:
            return None

        name = self.dict_google.get(lang)
        if name is None or name == "":
            return None
        return name

    def get_ms(self, lang):
        if self.dict_ms is None:
            return None

        name = self.dict_ms.get(lang)
        if name is None or name == "":
            return None
        return name

    def get_yandex(self, lang):
        if self.dict_yandex is None:
            return None

        name = self.dict_yandex.get(lang)
        if name is None or name == "":
            return None
        return name

    def get_deepl(self, lang):
        if self.dict_deepl is None:
            return None

        name = self.dict_deepl.get(lang)
        if name is None or name == "":
            return None
        return name
