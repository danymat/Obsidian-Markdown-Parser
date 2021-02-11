import re

class YamlParser:
    def __init__(self, fStream):
        self._regexAllYAML = r'(?<=---\n)(?:.*\n)+(?=---)'
        self._regexIterateYAML = r'(?:(\S+?):.*?\[(.+?)(?=\]))|(?:(\S+?):.*\n((?:-\s.*\n?)+))'
        self.fStream = fStream
        self.result = None
        self.yamlDict = {}
        
    def _findAllYAML(self, method, key=None):
        if key != None:
            self._regexFindKey = rf'(?:(?<={key}:).*?\[(.+?)(?=\]))|(?:(?<={key}:).*\n((?:-\s.*\n?)+))'

        # matches everything inside the frontmatter YAML (at least the first
        # occurence of --- this is matched ---)
        match = re.search(self._regexAllYAML, self.fStream)
        if match != None and method == "findvalue":
            self.result = match.group()
            return self._findValueInYAML()
        elif match != None and method == "iterate":
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
                        regex = re.compile(r'\b.+?\b')
                        new_result2 = result2.split(',')
                        for element in new_result2:
                            if len(element) > 1:
                                values = regex.findall(element)
                                string = ''
                                for value in values:
                                    string += value
                                valueSet.add(string)
                                #element = element.strip('\"')
                                #element = element.strip()
                                #valueSet.add(element)
                        self.yamlDict.update({result1 : valueSet})

                    # yaml list in current pair
                    elif result1 == '' and result2 == '':
                        valueSet = set()
                        regex = re.compile(r'\b.+?\b')
                        new_result4 = result4.split('\n')
                        for element in new_result4:
                            if len(element) > 1:
                                values = regex.findall(element)
                                string = ''
                                for value in values:
                                    string += value
                                valueSet.add(string)
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
            regex = re.compile(r'\b.+?\b')
            for element in new_result1:
                if len(element) > 1:
                    values = regex.findall(element)
                    string = ''
                    for value in values:
                        string += value
                    self.values.add(string)
        # Find all values in YAML with format
        # key:
        # - value1
        # - value2
        # ...
        elif result2 != None:
            new_result2 = result2.split('\n')
            regex = re.compile(r'\b.+?\b')
            for element in new_result2:
                if len(element) > 1:
                    values = regex.findall(element)
                    string = ''
                    for value in values:
                        string += value
                    self.values.add(string)
        return self.values
