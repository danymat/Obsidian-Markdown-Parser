import re
import os
from sys import argv
from src.MarkdownFile import MarkdownFile
from src.Parser import Parser
from src.Extractor import Extractor

if len(argv) not in [2,4,5]: raise Exception("Usage: python3 obsd_extract.py vault_folder --tag your_tag (-r)")
folder = argv[1]

parser = Parser(folderPath=folder)

if '--tag' in argv:
    tag = argv[argv.index('--tag') + 1]
    files = parser.searchFilesWithTag(tag)
else:
    tag = None
    files = parser.mdFiles


if '-r' in argv:
    files = parser.findSubFilesForFiles(files)

name = tag if tag else 'All'
Extractor._exportInZip(files, name)