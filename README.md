# How I would achieve the task ??
The workflow would be:

PDF 

Embedded-image extraction 

Image metadata 

Hashing 

Duplicate grouping

Unique-image folder 

Mapping report  

Validation

I would not screenshot pages. Instead, the program will access the PDF's embedded image objects directly and extract their available image streams. This preserves the embedded image data rather than introducing screenshot compression or scaling.And the mapping report would establish that image_003.jpg is the same extracted image as image_001.jpg, while image_005.jpg corresponds to image_002.png. For implementation, I would use a PDF-processing library capable of accessing embedded image streams, rather than converting PDF pages to images.

#	Subtask	Work	Estimate

1	Requirement confirmation-	Confirm PDF, duplicate definition, output structure	0.25 hr

2	PDF inspection-	Analyze PDF structure, pages, embedded objects and image types	0.5 hr

3	Extraction module-	Extract embedded images in original available format/resolution	1.0 hr

4	Metadata collection-	Capture page number, format, dimensions, size, object/reference information	0.5 hr

5	Exact duplicate detection-	Generate SHA-256 hashes and group identical image data	0.5 hr

6	Optional visual duplicate detection-	Perceptual hashing for visually identical/similar images	0.75 hr

7	Unique-image generation-	Retain one copy per duplicate group	0.5 hr

8	Mapping report-	Generate CSV/JSON mapping of source occurrences → retained images	0.75 hr

9	Validation-	Verify extracted count, hashes, dimensions and duplicate mappings	0.75 hr

10	Documentation-	README, execution instructions and output explanation	0.5 hr

Estimated total: 6 hours for the complete, tested implementation including optional perceptual duplicate detection.

If the requirement is strictly exact duplicate detection only, the estimated implementation time drops to roughly 4–4.5 hours.
