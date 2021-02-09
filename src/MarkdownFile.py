import re
from src.yamlParser import YamlParser

class MarkdownFile:
    def __init__(self, fileName, filePath):
        self._regexFindLinks = r'(?<=\[\[).*?(?=(?:\]\]|#|\|))' # Thanks to https://github.com/archelpeg
        self._regexFindYAML = r'(?:(?<=tags:\s\[)(.+?)(?=\]))|(?:(?<=tags:\n)((?:-\s\S*\n?)+))'
        self.fileName = fileName
        self.path = filePath
        self.tags = self._findTags()
        self.links = self._findLinksInCurrentFile()

    def _findTags(self) -> set:
        """Return a set of all tags in current file

        In order to retrieve a tag, it must be in one of the 3 formats:
        1. Simple format
        ```
        #tag1
        ```
        2. YAML array format
        ```
        tags: [tag1]
        ```
        3. Yaml list format
        ```
        tags:
        - tag1
        ```
        """
        value = None
        values = set()
        file = MarkdownFile
        file = self._openFile()
        self.fStream = file.read()
        file.close()

        # instantiate class
        findYAMLTags = YamlParser(self.fStream)
        # execute function to find tag in YamlParser
        values = findYAMLTags._findValueInYAML()

        # find simple tags
        simpleTags = re.compile(r"((?<=#)\S+)") # Find all tags in file with format #tag1 #tag2 ...
        # use opened file from instantiated YamlParser class
        result3 = simpleTags.findall(findYAMLTags.fStream)
        for tag in result3:
            # add simple tags to set() in YamlParser class
            values.add(tag)

        return values


    def _findLinksInCurrentFile(self) -> set:
        """Return the set of all links in the Current File (fileNames)"""
        file = self._openFile()
        fStream = file.read()
        file.close()
        return set(re.findall(self._regexFindLinks, fStream))

    def _openFile(self):
        """Open markdown file"""
        return open(self.path, "r", encoding="utf-8")
