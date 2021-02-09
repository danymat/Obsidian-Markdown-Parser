from src.Extractor import Extractor
from src.MarkdownFile import MarkdownFile
from src.Parser import Parser
from src.yamlParser import YamlParser
import os

def testMarkdownsRetrieval():
    parser = Parser('./test/testVault')
    assert len(parser.mdFiles) == 6

def testMarkdownTags():
    def nbFilesWithTag(parser, tag):
        return len([file for file in parser.mdFiles if tag in file.tags])

    parser = Parser('./test/testVault')
    for tag in ['tag2', 'tag1', 'inexistent']:
        files = parser.searchFilesWithTag(tag)
        assert len(files) == nbFilesWithTag(parser, tag)

def testSubfilesForFile():
    parser = Parser('./test/testVault')
    file = set([file for file in parser.mdFiles if file.fileName == 'file1.md'])
    subFiles = parser.findSubFilesForFiles(file)
    assert len(subFiles) == 3
