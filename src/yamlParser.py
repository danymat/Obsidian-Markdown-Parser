import re
from enum import Enum, auto

class YAML_METHOD(Enum):
    FIND_VALUE = auto()
    ITERATE = auto()

class YamlParser:
    def __init__(self, fStream):
        self._regexAllYAML = r'(?<=---\n)(?:.*\n)+(?=---)'
        self._regexIterateYAML = r'(?:(\S+?):.*?\[(.+?)(?=\]))|(?:(\S+?):.*\n((?:-\s.*\n?)+))'
        self.fStream = fStream
        self.result = None
        self.yamlDict = {}


    def findAllYAML(self, method: YAML_METHOD, key=None):
        if key != None:
            self._regexFindKey = rf'(?:(?<={key}:).*?\[(.+?)(?=\]))|(?:(?<={key}:).*\n((?:-\s.*\n?)+))'

        # matches everything inside the frontmatter YAML (at least the first
        # occurence of --- this is matched ---)
        match = re.search(self._regexAllYAML, self.fStream)
        if match != None and method == YAML_METHOD.FIND_VALUE:
            self.result = match.group()
            return self._findValueInYAML()
        elif match != None and method == YAML_METHOD.ITERATE:
            self.result = match.group()
            return self._iterateYAML()
        else:
            return None


    def _iterateYAML(self):
        # matches all yaml entries in self.result
        match = re.findall(self._regexIterateYAML, self.result)
        self.yamlDict = {}

        if match != None:
            for pair in match:
                # the results of the match groups will be saved here
                result1 = None
                result2 = None
                result3 = None
                result4 = None

                if pair != None:
                    # matches key in array syntax
                    result1 = pair[0]
                    # matches values in array syntax
                    result2 = pair[1]
                    # matches key in list syntax
                    result3 = pair[-2]
                    # matches values in list syntax
                    result4 = pair[-1]

                    # yaml array in current pair
                    if result3 == '' and result4 == '':
                    # Find all values in YAML with format key: [value1, value2,...]
                        valueSet = set()
                        new_result2 = result2.split(',')
                        for element in new_result2:
                            if len(element) > 1:
                                valueSet.add(self._yamlEntries("array", element))
                        self.yamlDict.update({result1 : valueSet})

                    # yaml list in current pair
                    elif result1 == '' and result2 == '':
                        valueSet = set()
                        new_result4 = result4.split('\n')
                        for element in new_result4:
                            if len(element) > 1:
                                valueSet.add(self._yamlEntries("list", element))
                        self.yamlDict.update({result3 : valueSet})


            return self.yamlDict


    def _findValueInYAML(self) -> set:
        """Return a set of all values stored in YAML

        In order to retrieve a value, it must be in one of the 2 formats:
        1. YAML array format
        ```
        key: [value1, value2]
        ```
        2. Yaml list format
        ```
        key:
        - value1
        ```
        """
        # all the values are stored in this set
        self.values = set()

        # matches the entry associated with the given key in the YAML from ._findAllYAML
        match = re.search(self._regexFindKey, self.result)
        result1 = None
        result2 = None

        if match != None:
            result1 = match.group(1)
            result2 = match.group(2)

        if result1 != None: # Find all values in YAML with format key: [value1, value2,...]
            new_result1 = result1.split(',')
            for element in new_result1:
                if len(element) > 1:
                    self.values.add(self._yamlEntries("array", element))
        # Find all values in YAML with format
        # key:
        # - value1
        # - value2
        # ...
        elif result2 != None:
            new_result2 = result2.split('\n')
            for element in new_result2:
                if len(element) > 1:
                    self.values.add(self._yamlEntries("list", element))
        return self.values


    def _yamlEntries(self, type, element):
        if type == "array":
            element = element.split()
            string = ''
            for part in range(len(element)):
                if element[part] == element[len(element) - 1]:
                    string += element[part]
                else:
                    string += element[part] + ' '
            string = string.strip('\"')
            return string
        elif type == "list":
            element = element.split()
            element.pop(0)
            string = ''
            for part in range(len(element)):
                if element[part] == element[len(element) - 1]:
                    string += element[part]
                else:
                    string += element[part] + ' '
            string = string.strip('\"')
            return string
        else:
            return None
