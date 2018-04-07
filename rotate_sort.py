# -*- coding: utf-8 -*-
import os

from PIL import Image

''' programe name: rotate_sort.py
    Last version : 2017.04.11.001
    1. 파일 목록작성 file_listing()
       file_list = []

    2. 앞부분 절반 180도 회전
       앞부분 절반은 홀수 페이지 뒷부분 절반은 짝수페이지
       스캔작업할때 1페이지 부터 스캔, 홀수 페이지가 시작페이지
       홀수페이지는 180도 회전, 손으로 자른 반대쪽이 기준이 되도록 스캔

    3. build rename command list
       홀수페이지는 p0001.jpg, p0003.jpg, p0005.jpg ... p0 < (전체 /2).jpg
       oddPageList= ['p0001.jpg', 'p0003.jpg', 'p0005.jpg', ]
       ['img_20170407_134552580_001.jpg', 'p0001.jpg'
        'img_20170407_134553515_002.jpg', 'p0003.jpg'
        'img_20170407_134554335_003.jpg', 'p0005.jpg'
        ...
        'img_20170407_134554335_161.jpg', 'p0321.jpg']

       짝수페이지는 p0002.jpg, p0004.jpg, p0006.jpg ... p0 < (전체 /2).jpg
       evenPageList= ['p0332.jpg', 'p0320.jpg', ... 'p0002.jpg',]
       ['img_20170407_134552580_162.jpg', 'p0322.jpg'
        'img_20170407_134553515_163.jpg', 'p0320.jpg'
        'img_20170407_134554335_164.jpg', 'p0318.jpg'
        ...
        'img_20170407_134554335_322.jpg', 'p0002.jpg']
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
    if filesCount % 2 != 0:
        print("{0}...오류: 작업중단!".format(filesCount))
        print("경고: 이미지파일이 홀수입니다.\
            \n양면작업 결과는 짝수가 정상이므로\
            \n작업대상을 확인하시기 바랍니다.")
        return
    # print("files...\n{0}".format(files))
    # file name listing
    file_list = []
    for file in files:
        if file.endswith(fileType):
            file_list.append(file)
    # print("{0} file(s) listed !".format(len(file_list)))
    print("The first entry in file_list: {}".format(file_list[0]))
    return file_list


# Rotate Odd pages by 180 degrees
def rotate(image_source, fileList):
    print("Rotating images...")
    for file in fileList:
        img = Image.open(os.path.join(image_source, file))
        img2 = img.rotate(180)
        img2.save(os.path.join(image_source, file))
    print("{0} images rotated".format(len(fileList)))


# rename and sort the scanned image files 
def rename_and_sort(fullList, fileType):
    fullListLength = len(fullList)
    firstHalfList = fullList[:int(len(fullList) / 2)]
    secondHalfList = fullList[int(len(fullList) / 2):]
    halfListLength = len(firstHalfList)

    if halfListLength != len(secondHalfList):
        print("Error: 홀수, 짝수 페이지의 수량이 다릅니다.\
              \n 작업대상 수량 확인바랍니다.")
        return

    # Build rename list for page ordering
    i = 0
    renameOrderList = []
    print("Building name list...")
    while i < fullListLength:
        # Odd Pages List
        for oddPage in range(1, halfListLength * 2, 2):
            temp_list = [fullList[i], "p{0:04}{1}".format(oddPage, fileType)]
            renameOrderList.append(temp_list)
            # print("{0} added.".format(temp_list))
            i += 1

        # Even Pages List - descending
        for evenPage in range(halfListLength * 2, 1, -2):
            temp_list = [fullList[i], "p{0:04}{1}".format(evenPage, fileType)]
            renameOrderList.append(temp_list)
            # print("{0} added".format(temp_list))
            i += 1
    # print("Rename table sample: {}".format(renameOrderList[0]))

    # Run file rename command
    if len(renameOrderList) >= 2:
        print("Renaming and sorting...")
        os.chdir(image_directory)
        for command in renameOrderList:
            os.rename(command[0], command[1])
        os.chdir("..")


# Listing
fullList = file_listing(file_extensions)

# Rotate firsthalf
rotate(image_directory, fullList[:int(len(fullList) / 2)])

# Build page ordering
rename_and_sort(fullList, file_extensions)
