#-*- coding: utf-8 -*-
import os
import glob

from PIL import Image

from fpdf import FPDF
from PyPDF2 import PdfFileReader, PdfFileMerger

''' programe name: PDFgen.py
    Last version : 2017.04.15.001
    2017.04.15.001 listing function replace from os.listdir to glob.glob
    2017.05.27.001 ImageList sorting 
    2017.05.27.002 input path check and if not exist use current directory as imput path

1. convert images to indivisual pdfs
2. merge all pdfs one file

''' 

# Working directory
image_directory="crop_output"
pdf_directory  ="pdf_output"
file_extensions=".jpg"
murged_fileName="final_merged, p"
# set margin
# margin이 Nono Zero 인 경우 아래처럼 양쪽에 설정
# pdf = FPDF(unit="pt", format=[width + 2*margin, height + 2*margin])
margin=0 # fit pdf to image, unit: pt

# Check input images path if not exist use current working directory from os.getcwd()
def ensure_input_path(source_path):
    if not os.path.exists(os.path.join(".", source_path)):
    	return os.getcwd()
    else:
    	return source_path


# Create PDF output path
def ensure_output_path(target_path):
    if not os.path.exists(os.path.join(".", target_path)):
        os.makedirs(target_path)
        print("'{}' directory created.".format(target_path))


# Create PDFs 
def convertImage2PDF(imagelist, pdf_directory):
	print("Converting images to PDF ...")
	for imageFile in imagelist:		
		cover=Image.open(imageFile)
		width, height = cover.size

		pdf=FPDF(unit="pt", format=[width, height])
		pdf.add_page()

		pdf.image(imageFile, margin, margin)

		filename_ext=os.path.split(imageFile)[1]        # "p0001.jpg"
		filenameOnly=os.path.splitext(filename_ext)[0]  # "p0001"
		filename    =filenameOnly+".pdf"                # "p0001.pdf"
		
		pdf.output(os.path.join(pdf_directory, filename), "F")


# Bind PDFs in one file
def bindPDF(pdf_dir, output_filename):
	print("Merging PDF files...")
	# pdf_files=[f for f in os.listdir(pdf_dir) if f.endswith("pdf")]
	pdf_files=glob.glob(pdf_dir+"/*.pdf")
	pageCount=len(pdf_files)

	merger = PdfFileMerger() 
	for file in pdf_files: 
		# merger.append(PdfFileReader(os.path.join(pdf_dir, file), "rb")) 
		merger.append(PdfFileReader(file, "rb")) 
	output_filename=output_filename+str(pageCount)+".pdf"
	
	# 결과물을 현재 디렉토리에 생성
	merger.write(output_filename)
	print("Done! '{0}' file created.".format(output_filename))


# "Run Main routine"
image_directory=ensure_input_path(image_directory)
imageList =sorted(glob.glob(image_directory+"/*"+file_extensions))

imageCount=len(imageList)
if imageCount> 0:
	ensure_output_path(pdf_directory)

	# Make PDF
	print("{0} images found in '{1}'".format(imageCount, image_directory))
	convertImage2PDF(imageList, pdf_directory)

	# Combind all pdfs to one
	bindPDF(pdf_directory, murged_fileName)
else:
	print("{0} images not found. Check '{1}' folder.".format(imageCount, image_directory))
