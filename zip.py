import zipfile

version = '0.0.0'
name = 'Boom-square-' + version

filename = 'file.zip'
fz = zipfile.ZipFile(filename, 'r')

for file in fz.namelist():
    fz.extract(file, './')

import os
import sys
import os.path
from shutil import copy

for dirpath, dirnames, filenames in os.walk(name):
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        print(filepath)
        copy(filepath, "F:/test/" + filename)
