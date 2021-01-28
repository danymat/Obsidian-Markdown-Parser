
import re
import os
from sys import argv
from zipfile import ZipFile

class Parser:
    def __init__(self, folderPath='.', tag=None):
        self._folderPath = folderPath
        self._tag = tag
        self._regexFindLinks = '(?<=\[\[).*(?=\]\])'
        self._regexFindTags = '#\S+'
        self._mdFiles = []
        self._called = False
        self._retrieveMarkdownFiles()
        self._currentFileAsHtml = None
        self._addedFiles = []

    def _retrieveMarkdownFiles(self):
        """
        Full credit goes to: https://github.com/archelpeg
        """
        if self._called: raise Exception('Files have already been retrieved')
        for dirpath, dirnames, files in os.walk(self._folderPath):
            # print(f'Found directory: {dirpath}')
            for file_name in files:
                if file_name.endswith('.md'):
                    #print(file_name)
                    # normalises path for current file system
                    normalised_path = os.path.normpath(dirpath + "/" + file_name)
                    self._mdFiles.append(normalised_path)
        self._called = True

    def _findFilesWithTag(self, tag=None):
        filesWithTag = []
        for file in self._mdFiles:
            self._openFileAsString(file)
            if self._tagInCurrentFile(tag):
                filesWithTag.append(file)
        return filesWithTag


    def _tagInCurrentFile(self, tag):
        tags = set(re.findall(self._regexFindTags, self._currentFileAsHtml))
        tags = [tag[1:] for tag in tags]
        return tag in tags

    def _findLinksInCurrentFile(self):
        return re.findall(self._regexFindLinks, self._currentFileAsHtml)

    def _openFileAsString(self, fileName):
        with open(fileName, "r", encoding="utf-8") as input_file:
            self._currentFileAsHtml = input_file.read()

    def _exportInZip(self, files, path=None):
        if len(files) == 0:
            print('No files found, exiting now'); return
        if path == None:
            path = '.'
            print('Exporting to current path...')
        else:
            print(f'Exporting to {path}...')
        zipObj = ZipFile(f'Exported_{self._tag}.zip', 'w')
        for file in files:
            zipObj.write(file)
        zipObj.close()

    def run(self):
        files = self._findFilesWithTag(self._tag)
        print(files)
        self._exportInZip(files)




if len(argv) != 4: raise Exception("Usage: python3 vault_folder --tag your_tag")
folder = argv[1]
tag = argv[3]
parser = Parser(folderPath=folder, tag=tag)
parser.run()








