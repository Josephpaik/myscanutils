#-*- coding: utf-8 -*-
import os
from PIL import Image

''' programe name: crop.py
    Last version : 2017.04.08.001
작성목적: 동일한 크기의 대량 이미지에서 같은 영역을 잘라내는 작업 자동화
'''
target_width   = 1694 	# 가로방향 크롭을 지정한다.
target_height  = 2572	# 세로방향 크롭을 지정한다. 
source_height  = 3040 	# JIS B5, B4용지, 300 DPI 선택한 경우 이미지 크기(height)
DPI=(300, 300)     		# 스캔 DPI와 동일
output_path    = "crop_output"
file_extensions= ".jpg"


# Crop 결과를 저장할 폴더 선택
def ensure_output_path(path):
    if not os.path.exists(os.path.join(".", path)):
        os.makedirs(path)


def crop_position_calc(source_height, width, height):
	'''	Crop 작업기준
	1. 스캔원본 
	   JIS B5용지를 300 DPI로 스캔하면 2150 x 3040 Pixel 이미지 생성
	   source_width  = 2150 # 사용 안함
	   source_height = 3040

	2. 크롭 사이즈
	   원하는 크롭영역의 크기가 width x height(예: 1722 x 2634) 이면
	   target_width  = 1722, target_height = 2634

	3. 잘라낼 폭(너비)
	   cut_width = source_width - target_width # 예: 2150 - 1722

	4. 잘라낼 높이
	   cut_height = (source_height - target_height) / 2 # 위아래로 이분

	5. 크롭 영역
	   crop_position = (0, cut_height,	target_width, target_height+cut_height)'''
	target_width = width 
	target_height= height
	cut_height	 = round((source_height-target_height)/2.0)
	crop_position= (0, cut_height, target_width, target_height+cut_height)

	# print("Cut_width    :{}".format(cut_width))
	# print("Cut_height   :{}".format(cut_height))
	# print("Crop_position:{}".format(crop_position))
	return crop_position


def page_crop(crop_position, fileType):
	currentFolderFiles=os.listdir(".")
	fileCount=len(currentFolderFiles)
	print("{0} file(s) found !".format(fileCount))
	print("Processing...")

	count=0
	for file in currentFolderFiles:
	    if file.endswith(fileType):
	        img =Image.open(file)
	        img2=img.crop(crop_position)

	        print("Saving: {0}".format(file))
	        img2.save(os.path.join(output_path, file), dpi=DPI) # DPI is not working
	        count+=1

	if count % 2 != 0:
		print("{0}...Warning!".format(count))
		print("이미지파일이 홀수입니다.\n \
		       양면작업 결과는 짝수가 정상이므로 \n \
		       작업대상을 확인하시기 바랍니다.")
	else:
		print("{0}...Done!".format(count))


# Run #
ensure_output_path(output_path)
crop_position=crop_position_calc(source_height, target_width, target_height)
page_crop(crop_position, file_extensions)