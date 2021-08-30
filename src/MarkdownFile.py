import re
from src.YamlParser import YamlParser, YAML_METHOD
from xml.etree.ElementTree import Element, ElementTree, SubElement

class MarkdownFile:
    def __init__(self, fileName, filePath):
        self._regexFindLinks = r'(?<=\[\[).*?(?=(?:\]\]|#|\|))' # Thanks to https://github.com/archelpeg
        self._regexFindHeaders = r'^\s*(#+)(\s+.*)'
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
        findYAMLTags = YamlParser(self.fStream)
        # execute method to find tag in YamlParser; in the called method another
        # method is called to find the specific tags
        # returns None if no YAML is found in a file
        values = findYAMLTags.findAllYAML(YAML_METHOD.FIND_VALUE, "tags")
        # if this is the case, then values is made a set so that the simple tags
        # can be added to it, because one can't add to NoneType
        if values == None:
            values = set()

        #############################
        # quick test for yaml iterator
        # yamlIterator = YamlParser(self.fStream)
        # print(yamlIterator.findAllYAML(YAML_METHOD.ITERATE))
        # print(self.fileName)
        #############################

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
    
    def toXML(self):
        file = self._openFile()
        lines = file.readlines()
        file.close()
        
        # Get the line numbers and header levels of each header
        section_lines = []
        section_levels = []
        section_titles = []
        for i, line in enumerate(lines):
            match = re.match(self._regexFindHeaders, line)
            if match is not None:
                section_lines.append(i)
                section_levels.append(len(match.group(1)))
                section_titles.append(match.group(2).strip())
        
        root = Element('root', {'level': '0'})
        parent_map = {}

        current_node = root
        section_ends = section_lines + [len(lines)]
        current_node.text = "".join(lines[:section_ends[0]])
        section_ends = section_ends[1:]

        for section_start, level, title, section_end in zip(section_lines, section_levels, section_titles, section_ends):
            while int(current_node.get('level')) >= level: 
                current_node = parent_map[current_node]
            section_node = SubElement(current_node, 'section', {'level': str(level), 'title': title})
            parent_map[section_node] = current_node
            section_node.text = "".join(lines[section_start:section_end])

            current_node = section_node
        
        return ElementTree(root)
    
def xmlToMarkdownText(tree: ElementTree):
    sections = []
    for node in tree.iter():
        if node.get('level') == '0':
            continue
        sections.append(node.text)
    
    return ''.join(sections)