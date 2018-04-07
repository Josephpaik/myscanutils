# -*- coding: utf-8 -*-
import os
from typing import Any, Tuple, Iterator

from PIL import Image

''' programe name: folderfix.py
원본 페이지 역순으로 구성된 폴더의 파일목록을 재구성하여 바로잡는 스크립트 
1. 폴더내 파일명 리스트 생성
2. fixed_output 폴더 생성
2. 리스트 길이 / 2 회 반복
   os.copy(1, rename_output\last)
   os.copy(2, rename_output\last - 1)
   os.copy(3, rename_output\last - 2)
'''

# Working directory
image_directory = "crop_output"
file_extensions = ".jpg"


# Image source file list up
def file_listing(fileType):
    print("Searching files in {0}".format(image_directory))
    files = os.listdir(image_directory)
    filesCount = len(files)
    print("{0} file(s) found !".format(filesCount))

    # print("files...\n{0}".format(files))
    # file name listing
    file_list = []
    for file in files:
        if file.endswith(fileType):
            file_list.append(file)
    # print("{0} file(s) listed !".format(len(file_list)))
    # print("The first entry in file_list: {}".format(file_list[0]))
    return file_list


# Flip all pages
def rotate(image_source, fileList):
    print("Rotating images...")
    for file in fileList:
        img = Image.open(os.path.join(image_source, file))
        img2 = img.rotate(180)
        img2.save(os.path.join(image_source, file))
    print("{0} images rotated".format(len(fileList)))


# rename for reversing the files
def reverse_rename(fullList, fileType):
    # Build rename command list for file name reordering
    fullListlen=len(fullList)
    new_filenamelist=[]
    reverse_filelist=reversed(fullList)

    print(" Building rename command list...")
    for i in range(fullListlen):
        new_filenamelist.append("f{0:04}{1}".format(i+1, fileType))

    renameOrderList: Iterator[Tuple[str, str]] = zip(reverse_filelist, new_filenamelist)
    print("renameOrderList: \n", renameOrderList)
    # for e in renameOrderList:
    #     print(e)

    # Run file rename command
    print("Renaming and sorting...")
    os.chdir(image_directory)
    for command in renameOrderList:
        os.rename(command[0], command[1])
    os.chdir("..")


# Listing
fullList = file_listing(file_extensions)

# Flip pages
# rotate(image_directory, fullList[::])

# Reversing pages
reverse_rename(fullList, file_extensions)