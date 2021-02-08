# Obsidian Extractor (obsd_extract)

![(Github All Releases)](https://img.shields.io/github/downloads/danymat/Obsidian-Extractor/total)

This script will create a zip of your vault, depending on the options you select.

## Motives

I like to keep my vault with only one folder inside. That means, it's a pain to copy only relevant files!

## State of the Art

At the moment, it supports:

- Creating a zip file from a specified vault with a specific tag, with optional link following (YAML support)
- Creating a zip file from the entire vault

## Usage

```bash
python obsd_extract.py vaultFolder --tag yourTag
```

If you would like to follow links, add `-r` option at the end:

```bash
python obsd_extract.py vaultFolder --tag yourTag -r
```

If you would like to export all vault:

```bash
python obsd_extract.py vaultFolder
```

## Extended

At the moment, I have implemented a basic parsing library.

### Parser

- Usage

```python
from src.Parser import Parser
parser = Parser('/path/to/vault')
```

#### Attributes

- `mdFiles` Array of MarkdownFile in vault
#### Methods

- `findSubFilesForFiles(files)` returns a set of `MarkdownFile` linked with the **set** of `MarkdownFile` specified
- `searchFilesWithTag(tag)` returns a set of `MarkdownFile` with a specified tag

### MarkdownFile

#### Attributes

- `fileName` file name (string) of the current markdown file, with `.md` extension (e.g `'file.md'`)
- `path` relative path (string) of the current markdown file (e.g `'testVault/file.md'`)
- `tags` set of tags in current file (e.g `{'tag2', 'tag3'}`)
- `links` set of links in markdown files (e.g `{'file2'}`)

### Examples

```python
parser = Parser('test/testVault')
```

- Find all fileNames that doesn't have a tag

```python
fileWithoutTags = [file.fileName for file in parser.mdFiles if len(file.tags) == 0]
```

- Find all files that have `tag1` in them

```python
filesWithSpecificTag = [file for file in parser.mdFiles if 'tag1' in file.tags]
# OR
filesWithSpecificTag = parser.searchFilesWithTag('tag1')
```

## Roadmap

New features I intent to add:

- [X] Exporting full vault
- [ ] Exporting vault from multiple tags


## Contributing

If you would like to add shiny new features, or correct bugs I unfortunately added, please fork
this repository, and create a pull request from it.
