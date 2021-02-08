import re

class MarkdownFile:
    def __init__(self, fileName, filePath):
        self._regexFindTags = '#\S+'
        self._regexFindLinks = '(?<=\[\[).*?(?=(?:\]\]|#|\|))' # Thanks to https://github.com/archelpeg
        self.fileName = fileName
        self.path = filePath
        self.tags = self._findTags()
        self.links = self._findLinksInCurrentFile()

    def _findTags(self) -> set:
        file = self._openFile()
        fStream = file.read()
        file.close()
        tags = set(re.findall(self._regexFindTags, fStream))
        return [tag[1:] for tag in tags]


    def _findLinksInCurrentFile(self) -> set:
        """Return all links in the Current File"""
        file = self._openFile()
        fStream = file.read()
        file.close()
        return set(re.findall(self._regexFindLinks, fStream))

    def _openFile(self):
        """Open one file and store the content in _currentFileAsHtml"""
        return open(self.path, "r", encoding="utf-8")
