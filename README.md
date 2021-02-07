# Obsidian Extractor (obsd_extract)

![(Github All Releases)](https://img.shields.io/github/downloads/danymat/Obsidian-Extractor/total)

This script will create a zip of your vault, depending on the options you select.

Made by Daniel Mathiot.

## Motives

I like to keep my vault with only one folder inside. That means, it's a pain to copy only relevant files!

## State of the Art

At the moment, it supports:

- Creating a zip file from a specified vault with a specific tag, with optional link following
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

## Roadmap

New features i intent to add:

- [X] Exporting full vault
- [ ] Exporting vault from multiple tags

## Contributing

If you would like to add shiny new features, or correct bugs I unfortunately added, please fork
this repository, and create a pull request from it.
