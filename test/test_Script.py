from src.MarkdownFile import xmlToMarkdownText
from src.Parser import Parser
from test.xml_helpers import loadXMLSingleLevelHeaders, loadXMLMultiLevelHeaders, loadXMLFalseHeaders, loadXMLEmptyFile, loadXMLNoSection, treesEqual

def testMarkdownsRetrieval():
    parser = Parser('./test/testVault')
    assert len(parser.mdFiles) == 11

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

def testXMLBuilderSingleLevelHeaders():
    parser = Parser('./test/testVault')
    file = [file for file in parser.mdFiles if file.fileName == 'single-level-headers.md'].pop()
    assert treesEqual(file.toXML(), loadXMLSingleLevelHeaders())

def testXMLBuilderMultiLevelHeaders():
    parser = Parser('./test/testVault')
    file = [file for file in parser.mdFiles if file.fileName == 'multi-level-headers.md'].pop()
    assert treesEqual(file.toXML(), loadXMLMultiLevelHeaders())

def testXMLBuilderFalseHeaders():
    parser = Parser('./test/testVault')
    file = [file for file in parser.mdFiles if file.fileName == 'false-headers.md'].pop()
    assert treesEqual(file.toXML(), loadXMLFalseHeaders())

def testXMLBuilderEmptyFile():
    parser = Parser('./test/testVault')
    file = [file for file in parser.mdFiles if file.fileName == 'empty-file.md'].pop()
    assert treesEqual(file.toXML(), loadXMLEmptyFile())

def testXMLBuilderNoSectionFile():
    parser = Parser('./test/testVault')
    file = [file for file in parser.mdFiles if file.fileName == 'no-section.md'].pop()
    assert treesEqual(file.toXML(), loadXMLNoSection())

def testXMLWriterSingleLevelHeaders():
    parser = Parser('./test/testVault')
    file = [file for file in parser.mdFiles if file.fileName == 'single-level-headers.md'].pop()
    with open(file.path, 'r') as mdFile:
        text = mdFile.read()
    
    xmlToMarkdownText(loadXMLSingleLevelHeaders()) == text

def testXMLWriterMultiLevelHeaders():
    parser = Parser('./test/testVault')
    file = [file for file in parser.mdFiles if file.fileName == 'multi-level-headers.md'].pop()
    with open(file.path, 'r') as mdFile:
        text = mdFile.read()
    
    xmlToMarkdownText(loadXMLMultiLevelHeaders()) == text

def testXMLWriterFalseHeaders():
    parser = Parser('./test/testVault')
    file = [file for file in parser.mdFiles if file.fileName == 'false-headers.md'].pop()
    with open(file.path, 'r') as mdFile:
        text = mdFile.read()
    
    xmlToMarkdownText(loadXMLFalseHeaders()) == text

def testXMLWriterEmptyFile():
    parser = Parser('./test/testVault')
    file = [file for file in parser.mdFiles if file.fileName == 'empty-file.md'].pop()
    with open(file.path, 'r') as mdFile:
        text = mdFile.read()
    
    xmlToMarkdownText(loadXMLEmptyFile()) == text

def testXMLWriterNoSectionFile():
    parser = Parser('./test/testVault')
    file = [file for file in parser.mdFiles if file.fileName == 'no-section.md'].pop()
    with open(file.path, 'r') as mdFile:
        text = mdFile.read()
    
    xmlToMarkdownText(loadXMLNoSection()) == text

