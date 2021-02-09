import re

class YamlParser:
    def __init__(self, key, fStream):
        self._regexFindYAML = rf'(?:(?<={key}:\s\[)(.+?)(?=\]))|(?:(?<=tags:\n)((?:-\s\S*\n?)+))'
        self.fStream = fStream
        
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


        match = re.search(self._regexFindYAML, self.fStream)
        result1 = None
        result2 = None

        if match != None:
            result1 = match.group(1)
            result2 = match.group(2)

        if result1 != None: # Find all values in YAML with format key: [value1, value2,...]
            new_result1 = result1.split(',')
            for element in new_result1:
                self.values.add(element.strip())

        # Find all values in YAML with format
        # key:
        # - value1
        # - value2
        # ...
        elif result2 != None:
            result2 = result2.strip('\n')
            result2 = result2.split()
            for element in result2:
                if element != '-':
                    self.values.add(element)

        return self.values