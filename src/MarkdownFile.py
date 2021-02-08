import re

class MarkdownFile:
    def __init__(self, fileName, filePath):
        self._regexFindLinks = r'(?<=\[\[).*?(?=(?:\]\]|#|\|))' # Thanks to https://github.com/archelpeg
        self._regexFindTags = r'(?:(?<=tags:\s\[)(.+?)(?=\]))|(?:(?<=tags:\n)((?:-\s\S*\n?)+))'
        self.fileName = fileName
        self.path = filePath
        self.tags = self._findTags()
        self.links = self._findLinksInCurrentFile()

    def _findTags(self) -> set:
        tag= None
        tags = set()
        file = self._openFile()
        fStream = file.read()
        file.close()

        match = re.search(self._regexFindTags, fStream)
        result1 = None
        result2 = None

        if match != None:
            result1 = match.group(1)
            result2 = match.group(2)

        if result1 != None: # Find all tags in YAML with format tags: [tag1, tag2,...]
            new_result1 = result1.split(',')
            for tag in new_result1:
                tags.add(tag)

        # Find all tags in YAML with format
        # tags:
        # -tag1
        # -tag2
        # ...
        elif result2 != None:

            result2 = result2.strip('\n')
            result2 = result2.split()
            print(result2)
            for element in result2:
                if element != '-':
                    tags.add(element)

        simpleTags = re.compile(r"((?<=#)\S+)") # # Find all tags in file with format #tag1 #tag2 ...
        result3 = simpleTags.findall(fStream)
        for tag in result3:
            tags.add(tag)

        return tags


    def _findLinksInCurrentFile(self) -> set:
        """Return all links in the Current File"""
        file = self._openFile()
        fStream = file.read()
        file.close()
        return set(re.findall(self._regexFindLinks, fStream))

    def _openFile(self):
        """Open one file and store the content in _currentFileAsHtml"""
        return open(self.path, "r", encoding="utf-8")
