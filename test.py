#!/usr/bin/env python
from __future__ import with_statement
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import os, zipfile

def zipfolder(path, relname, archive):
    paths = os.listdir(path)
    for p in paths:
        p1 = os.path.join(path, p)
        p2 = os.path.join(relname, p)
        archive.write(p1, p2)
        if os.path.isdir(p1):
            zipfolder(p1, p2, archive)

def create_zip(path, relname, archname):
    archive = zipfile.ZipFile(archname, "w", zipfile.ZIP_DEFLATED)
    if os.path.isdir(path):
        zipfolder(path, relname, archname)
    else:
        archive.write(path, relname)
    archive.close()

compressedFile = zipfile.ZipFile("result.zip","w", zipfile.ZIP_DEFLATED)

zipfolder("/home/navaro/dev/py/jag/result", "/", compressedFile);