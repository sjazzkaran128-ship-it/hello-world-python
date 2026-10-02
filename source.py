
import pymupdf
import hashlib
import os
import csv
import imagehash
from PIL import Image
from io import BytesIO
pdf_path = r"C:\Users\sjazz\Downloads\identical duplicate.pdf"
pdf = pymupdf.open(pdf_path)
os.makedirs("identical_images", exist_ok=True)
os.makedirs("duplicate_images", exist_ok=True)
seen_hashes = set()
seen_phashes = []
report = []
image_number = 1
for page_number, page in enumerate(pdf, start=1):
    print("Checking page:", page_number)
    images = page.get_images()
    for image in images:
        xref = image[0]
        data = pdf.extract_image(xref)
        image_bytes = data["image"]
        extension = data["ext"]
        sha_hash = hashlib.sha256(
            image_bytes
        ).hexdigest()
        img = Image.open(BytesIO(image_bytes))
        phash = imagehash.phash(img)
        filename = f"image_{image_number}.{extension}"
        status = ""
        folder = ""
        if sha_hash in seen_hashes:
            status = "Identical"
            folder = "identical_images"
            print("Identical image found!")
        else:
            duplicate_found = False
            for old_hash in seen_phashes:
                difference = phash - old_hash
                if difference <= 5:
                    duplicate_found = True
                    break
            if duplicate_found:
                status = "Duplicate"
                folder = "duplicate_images"
                print("Visual duplicate found!")
            seen_hashes.add(sha_hash)
            seen_phashes.append(phash)
        image_path = os.path.join(folder,filename)
        with open(image_path, "wb") as file:
            file.write(image_bytes)
        report.append([page_number,filename,extension,sha_hash,str(phash),status,folder])
        image_number += 1
pdf.close()
report_path = os.path.join(os.getcwd(), "mapping_report_new1.csv")
with open(report_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Page", "Image Name", "Format", "SHA256","Perceptual Hash", "Status", "Saved Folder"])
    writer.writerows(report)
print("Report saved at:", report_path)
identical_count = sum(
    1 for row in report if row[5] == "Identical"
)
duplicate_count = sum(
    1 for row in report if row[5] == "Duplicate"
)
print("Total images:", len(report))
print("Identical images:", identical_count)
print("Visual duplicates:", duplicate_count)
print("\nImages saved in separate folders.")
print("Mapping report: mapping_report_new1.csv")