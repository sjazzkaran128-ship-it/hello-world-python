import pymupdf
import hashlib
import imagehash
import csv
import os
from PIL import Image
from io import BytesIO
folder = r"C:\Users\sjazz\OneDrive\Desktop\Hello World"
pdf_path = r"C:\Users\sjazz\OneDrive\Desktop\Hello World\sample-1000pages.pdf"
pdfs = [
    f for f in os.listdir(folder)
    if f.lower().endswith(".pdf")
]
print("PDF files found:", pdfs)
if not pdfs:
    raise FileNotFoundError("No PDF found in the folder.")
folder = os.path.join(folder, pdfs[0])
print("Using PDF:", folder)
output = "image_extraction_output"
os.makedirs(output, exist_ok=True)
os.makedirs(f"{output}/identical_images", exist_ok=True)
os.makedirs(f"{output}/duplicate_images", exist_ok=True)
pdf = pymupdf.open(folder)
print("PDF opened successfully!")
print("Pages:", len(pdf))
sha_hashes = set()
phashes = []
image_number = 1
identical = 0
duplicate = 0
report_path = f"{output}/mapping_report.csv"
with open(report_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Page","XREF","Image","Format","SHA256","pHash","Status","Folder"])
    for page_number, page in enumerate(pdf, 1):
        print(f"Checking page {page_number}...")
        page_xrefs = set()
        for image in page.get_images():
            xref = image[0]
            if xref in page_xrefs:
                continue
            page_xrefs.add(xref)
            try:
                data = pdf.extract_image(xref)
                image_bytes = data["image"]
                extension = data["ext"]
                sha = hashlib.sha256(image_bytes).hexdigest()
                img = Image.open(BytesIO(image_bytes))
                phash = imagehash.phash(img)
                if sha in sha_hashes:
                    status = "Identical"
                    folder = "identical_images"
                    identical += 1
                else:
                    status = "Duplicate"
                    folder = "duplicate_images"
                    duplicate += 1
                filename = (
                    f"page_{page_number}_"
                    f"image_{image_number}."
                    f"{extension}"
                )
                with open(
                    f"{output}/{folder}/{filename}","wb") as out:
                    out.write(image_bytes)
                sha_hashes.add(sha)
                phashes.append(phash)
                writer.writerow([page_number,xref,filename,extension,sha,str(phash),status,folder])
                image_number += 1
            except Exception as e:
                print(
                    f"Error on page {page_number}, "
                    f"XREF {xref}: {e}"
                )
pdf.close()
print("\n" + "=" * 50)
print("Processing completed.")
print("=" * 50)
print(f"Total processed : {image_number - 1}")
print(f"Identical       : {identical}")
print(f"Duplicates      : {duplicate}")
print(f"\nReport saved at:")
print(os.path.abspath(report_path))