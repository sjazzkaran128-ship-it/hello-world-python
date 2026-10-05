# How I would achieve the task ??
The workflow would be:

PDF:- First of all we choose the pdf from the web browser

Embedded-image extraction: After we will do the image extraction of identical as well as duplicate images with the help of pymupdf library of python which is used to extract image from each page of the pdf

Image metadata- After that the image metadata of both the extracted images are being compared in order to perform hashing . In this meta data there is very several useful information regarding the images , ie about the page number of image, the size of the image, the resolution and quality of the image,and weather the image is identical or duplicate

Hashing- Hashing is used to identify the identical and duplicate images. it is a powerful tool to pick up the identical images and from the duplicate. In these program we make use of sha 256hash and perceptual hash . sha 256 is used for identifying the identical and duplicate images while perceptual hash is used to seperate identical from duplicate. During the hashing it is important to note the hash period in order to facilitate image grouping

Duplicate grouping: In this there is grouping of all the duplicate images in a seperate folder so that if coudn't be mix up with the identical images as there is a mere difference b/w the identical and duplicate images. Seperate all the duplicate images in another folder

Identical-image folder Now left the part of unique images. Make a another folder and put all the identical images there

Mapping report- the mapping report will give you the list of all the duplicate and identical images along with their status and the folder in which they are saved . the reports is in the form of csv file in which all the data is saved in terms of spreadsheets  

Validation : The last step is to check weather the process is being performed successfully or not

I would not screenshot pages. Instead, the program will access the PDF's embedded image objects directly and extract their available image streams. This preserves the embedded image data rather than introducing screenshot compression or scaling.

And the mapping report would establish that image_2.jpg is the same extracted image as image_1.jpg, while image_3.jpg corresponds to image_002.png. For implementation, I would use a PDF-processing library capable of accessing embedded image streams, rather than converting PDF pages to images.

#	Subtask	Work	

1	Requirement confirmation-	Confirm PDF, duplicate definition, output structure

2	PDF inspection-	Analyze PDF structure, pages, embedded objects and image types

3	Extraction module-	Extract embedded images in original available format/resolution

4	Metadata collection-	Capture page number, format, dimensions, size, object/reference information

5	Exact duplicate detection-	Generate SHA-256 hashes and group identical image data

6	Optional visual duplicate detection-	Perceptual hashing for visually identical/similar images

7	Unique-image generation-	Retain one copy per duplicate group

8	Mapping report-	Generate CSV/JSON mapping of source occurrences → retained images

9	Validation-	Verify extracted count, hashes, dimensions and duplicate mappings

10	Documentation-	README, execution instructions and output explanation

# Challenges Faced During Extraction of 1000s of identical duplicate images

1 Python program may become slow to run as many images and perceptual hashes may be kept in the memory during processing

2 Visually identical images may be classified as different bcs sha 256 detects identical images

3 The script may extract and save the same image repeatedly as pymupdf lib can may reuse the same image on several pages

4 The disc usage increases and the output folder becomes difficult to manage as saving each occurence can create thousands of file

5 Files may overwrite themselves or script may fail as giving simple names of images may already exist from previous run

6 yThe script may fail due to the permission error or produce an incomplete report due to large reports take longer to write content

7 It leads to unclear duplicate grouping as it becomes difficult to trace an image back to its source page
