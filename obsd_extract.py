import re
import os
from sys import argv
from zipfile import ZipFile
from typing import List

class MarkdownFile:
    def __init__(self, fileName, filePath):
        self._regexFindTags = '#\S+'
        self._regexFindLinks = '(?<=\[\[).*?(?=(?:\]\]|#|\|))' # Thanks to https://github.com/archelpeg
        self.fileName = fileName
        self._path = filePath
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
        return open(self._path, "r", encoding="utf-8")

class Parser:
    def __init__(self, folderPath='.'):
        self._folderPath = folderPath
        self.mdFiles = list[MarkdownFile]
        self._retrieveMarkdownFiles()


    def _retrieveMarkdownFiles(self):
        """Directory traversal to find all .md files and stores them in _mdFiles

        Full credit goes to: https://github.com/archelpeg
        """
        self.mdFiles = []
        for dirpath, dirnames, files in os.walk(self._folderPath):
            # print(f'Found directory: {dirpath}')
            for file_name in files:
                if file_name.endswith('.md'):
                    normalised_path = os.path.normpath(dirpath + "/" + file_name) # normalises path for current file system
                    file = MarkdownFile(file_name, normalised_path)
                    self.mdFiles.append(file)

    def searchFilesWithTag(self, tag=None):
        """Find all files containing a specific tag
        """
        files = set()
        if tag == None:
            return files
        for file in self.mdFiles:
            if tag in file.tags:
                files.add(file)
        return files

    def findSubFilesForFiles(self, files: set):
        """Iteration to grow files while i can"""
        while not self._grow(files):
            pass
        return files


    def _grow(self, files):
        """Add new files found following links in files and stores them in files"""
        addedFiles = set()
        for file in files:
            linkedFiles = file.links
            linkedFiles = [link+'.md' for link in linkedFiles] # Added .md at the end
            linkedFiles = [file # Get the full links
                for file in self.mdFiles
                for link in linkedFiles
                if link in file.fileName
            ]
            linkedFiles = set(linkedFiles) - files # Only keep not added files
            for link in linkedFiles:
                addedFiles.add(link)
        for file in addedFiles:
            files.add(file)
        return len(addedFiles) == 0

class Extractor:

    @classmethod
    def _exportInZip(cls, files, zipName, path=None):
        """Export all files in zip, if path not specified, export to current location"""
        if len(files) == 0:
            print('No files found, exiting now'); return
        if path == None:
            path = '.'
            print('Exporting to current path...')
        else:
            print(f'Exporting to {path}...')

        zipObj = ZipFile(f'Exported_{zipName}.zip', 'w')
        print('###### FILES FOUND ######')
        for file in files:
            print(file.fileName)
            zipObj.write(file.fileName, os.path.join('.',file.fileName)) # Not sure if it recreates subfolders
        zipObj.close()
        print('######################')
        print(f'Exported! {len(files)} notes')




if len(argv) not in [2,4,5]: raise Exception("Usage: python3 obsd_extract.py vault_folder --tag your_tag (-r)")
folder = argv[1]

if '--tag' in argv:
    tag = argv[argv.index('--tag') + 1]
else:
    tag=None

parser = Parser(folderPath=folder)

files = parser.searchFilesWithTag(tag)
print(files)
if len(files) == 0:
    files = []

if '-r' in argv:
    files = parser.findSubFilesForFiles(files)

name = tag if tag else 'All'
print(files)
Extractor._exportInZip(files, name)