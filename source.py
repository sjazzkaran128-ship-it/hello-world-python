import builtins
import pymupdf
import hashlib
import imagehash
import csv
import os
from PIL import Image
from io import BytesIO
folder = r"C:\Users\sjazz\OneDrive\Desktop\Hello World"
pdf_path = r"C:\Users\sjazz\OneDrive\Desktop\Hello World\sample-100pages.pdf"
pdfs = [
    entry.name
    for entry in os.scandir(folder)
    if entry.is_file() and entry.name.lower().endswith(".pdf")
]
builtins.print("PDF files found:", pdfs)
if not pdfs:
    raise FileNotFoundError("No PDF found in the folder.")
folder = os.path.join(folder, pdfs[0])
builtins.print("Using PDF:", folder)
pdf = pymupdf.open(folder)
builtins.print("PDF opened successfully!")
builtins.print("Pages:", len(pdf))
output = "image_extraction_output"
os.makedirs(output, exist_ok=True)
os.makedirs(f"{output}/identical_images", exist_ok=True)
os.makedirs(f"{output}/duplicate_images", exist_ok=True)
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
        builtins.print(f"Checking page {page_number}")
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
                    f"page {page_number}_"
                    f"image {image_number}."
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
                builtins.print(
                    f"Error on page {page_number}, "
                    f"XREF {xref}: {e}"
                )
pdf.close()
builtins.print("\n" + "=" * 50)
builtins.print("Processing completed.")
builtins.print("=" * 50)
builtins.print(f"Total processed : {image_number - 1}")
builtins.print(f"Identical       : {identical}")
builtins.print(f"Duplicates      : {duplicate}")
builtins.print(f"Report saved at:")
builtins.print(os.path.abspath(report_path))