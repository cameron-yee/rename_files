#!/usr/local/bin/python3
import sys
import os
from glob import glob
import string
import re
import time

def stripPunctuation(name):
    x = string.punctuation.replace('_','')
    punct = x.replace('.','')
    table = str.maketrans('', '', punct)
    final_name = name.translate(table)
    return final_name


def removeDoubleFileType(name_2):
    final_name = re.sub('docx.pdf$','pdf', name_2)   
    return final_name


def renameFile(f, count):
    try:
        base = os.path.basename(f)
        base_lower = base.lower()
        name = base_lower.replace(' ','_') 
        name_2 = stripPunctuation(name)

        final_name = removeDoubleFileType(name_2)

        dirname = os.path.dirname(f)
        sf = str(f)
        sdn = str(dirname + '/' + final_name)
        os.rename(sf,sdn)
    except(FileNotFoundError):
        if count < 500:
            time.sleep(10)
            count += 1
            renameFile(f, count)
        else:
            print('Download took too long to rename.  Possible download failure.')


def getFilePaths(directory):
    files = []
    dir_files = os.listdir(directory)
    relevant_files = [f for f in dir_files if f not in ['.rename_files.py', '.DS_Store', '.localized']]

    for f in relevant_files:
        files.append(directory + '/{}'.format(f))

    return files


if __name__ == '__main__':
    #Hardcoded to automate with fswatch
    directory = '/Users/cyee/Downloads'
    files = getFilePaths(directory)
    count = 0
    for f in files:
        renameFile(f, count)
