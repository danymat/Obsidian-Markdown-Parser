from zipfile import ZipFile
import os

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

        zipName = zipName.replace('/', '-')

        zipObj = ZipFile(f'Exported_{zipName}.zip', 'w')
        print('###### FILES FOUND ######')
        for file in files:
            print(file.fileName)
            zipObj.write(file.path, os.path.join('.',file.fileName)) # Not sure if it recreates subfolders
        zipObj.close()
        print('######################')
        print(f'Exported! {len(files)} notes')