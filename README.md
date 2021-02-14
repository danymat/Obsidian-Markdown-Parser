# Obsidian Markdown Parser

![(Github All Releases)](https://img.shields.io/github/downloads/danymat/Obsidian-Extractor/total)

This repository will give you tools to parse and fetch useful informations of your notes in your Obsidian vault.

## Motives

I like to do some python scripts with my vault, so this repository is the tool I needed in order to parse my Markdown files.

## State of the Art

At the moment, I have implemented a basic parsing library.

### Parser

#### Usage

```python
from src.Parser import Parser
parser = Parser('/path/to/vault')
```

#### Attributes

- `mdFiles` Array of MarkdownFile in vault

#### Methods

- `findSubFilesForFiles(files)` returns a set of `MarkdownFile` linked with the **set** of `MarkdownFile` specified
- `searchFilesWithTag(tag)` returns a set of `MarkdownFile` with a specified tag


### YamlParser

#### Usage

```python
from src.yamlParser import YamlParser, YAML_METHOD

# the file contents need to be read
file = MarkdownFile
file = self._openFile()
self.fStream = file.read()
file.close()

findYAMLTags = YamlParser(self.fStream)
# find all values for a particular key
# this will return a set with the values that have "tags" as key
values = findYAMLTags.findAllYAML(YAML_METHOD.FIND_VALUE, "tags")


yamlIterator = YamlParser(self.fStream)
# return all keys and values as a dictionary with the key as string and its values as set
print(yamlIterator.findAllYAML(YAML_METHOD.ITERATE))
```

#### Methods

- `.findAllYAML()` with the parameters `YAML_METHOD.FIND_VALUE` and `"{key}"` with `{key}`
  as the YAML key returns the associated values as a set
- `.findAllYAML()` with the parameter `YAML_METHOD.ITERATE` will return all key-value
  pairs in YAML as a dictionary with the key as a string and its associated
  values as a set

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


- [ ] Add more tests 
- [ ] Ignore .obsidian/ folder


## Contributing

If you would like to add shiny new features, or correct bugs I unfortunately added, please fork
this repository, and create a pull request from it. Below is the list of all contributors for this repository, if you contributed please consider adding your name !

Contributors:

- Daniel Mathiot ([danymat](https://github.com/danymat))
- Christian Körtner ([archelpeg](https://github.com/archelpeg))

