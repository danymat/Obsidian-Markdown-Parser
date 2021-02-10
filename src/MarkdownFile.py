import re
from src.yamlParser import YamlParser

class MarkdownFile:
    def __init__(self, fileName, filePath):
        self._regexFindLinks = r'(?<=\[\[).*?(?=(?:\]\]|#|\|))' # Thanks to https://github.com/archelpeg
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
        # this block needs to be set by each method that wants to retrieve YAML
        # values; when instantiating in YamlParser I had circular dependencys
        file = MarkdownFile
        file = self._openFile()
        self.fStream = file.read()
        file.close()

        # instantiate YamlParser class
        # the only thing passed to the class are the contents from above of every looped
        # file in the Parser class (example in .searchFilesWithTag())
        # the key has to be given as first argument in a string without the colon
        findYAMLTags = YamlParser("tags", self.fStream)
        # execute method to find tag in YamlParser; in the called method another
        # method is called to find the specific tags
        # returns None if no YAML is found in a file
        values = findYAMLTags._findAllYAML("findvalue")
        # if this is the case, then values is made a set so that the simple tags
        # can be added to it, because one can't add to NoneType
        if values == None:
            values = set()


        # find simple tags
        simpleTags = re.compile(r"((?<=#)\S+)") # Find all tags in file with format #tag1 #tag2 ...
        result3 = simpleTags.findall(self.fStream)
        for tag in result3:
            # add simple tags to set()
            values.add(tag)

        # a set of all values (here: tags) is returned; a method in
        # Parser.py then checks if the entered tag is part of it
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
