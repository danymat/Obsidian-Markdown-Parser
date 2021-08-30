import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree

def treesEqual(t1: ElementTree, t2: ElementTree) -> bool:
    return ET.canonicalize(ET.tostring(t1.getroot())) == ET.canonicalize(ET.tostring(t2.getroot()))

def loadXMLSingleLevelHeaders(): 
    return ET.parse('./test/testVault/xml_markdown_tests/expected_outputs/single-level-headers.xml')

def loadXMLMultiLevelHeaders(): 
    return ET.parse('./test/testVault/xml_markdown_tests/expected_outputs/multi-level-headers.xml')

def loadXMLFalseHeaders(): 
    return ET.parse('./test/testVault/xml_markdown_tests/expected_outputs/false-headers.xml')

def loadXMLEmptyFile(): 
    return ET.parse('./test/testVault/xml_markdown_tests/expected_outputs/empty-file.xml')

def loadXMLNoSection(): 
    return ET.parse('./test/testVault/xml_markdown_tests/expected_outputs/no-section.xml')
