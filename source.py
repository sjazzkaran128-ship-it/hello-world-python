import pymupdf
import hashlib
import os
import csv
pdf_path = "C:/Users/sjazz/Downloads/identical duplicate.pdf"
pdf = pymupdf.open(pdf_path)

print("PDF opened successfully!")
print("Number of pages:", len(pdf))


# --------------------------------
# 2. Create output folder
# --------------------------------

os.makedirs("images", exist_ok=True)


# --------------------------------
# 3. Store hashes
# --------------------------------

seen = set()

report = []

image_number = 1


# --------------------------------
# 4. Read every page
# --------------------------------

for page_number, page in enumerate(pdf, start=1):

    print("Checking page:", page_number)

    images = page.get_images()

    for image in images:

        # Get image ID
        xref = image[0]

        # Extract image
        data = pdf.extract_image(xref)

        image_bytes = data["image"]

        extension = data["ext"]


        # --------------------------------
        # 5. Create hash
        # --------------------------------

        image_hash = hashlib.sha256(
            image_bytes
        ).hexdigest()


        # --------------------------------
        # 6. Check duplicate
        # --------------------------------

        if image_hash in seen:

            status = "Duplicate"

            print("Duplicate image found!")

        else:

            status = "Unique"

            print("Unique image found!")

            # Remember hash
            seen.add(image_hash)


            # --------------------------------
            # 7. Save image
            # --------------------------------

            filename = (
                f"image_{image_number}.{extension}"
            )

            image_path = os.path.join(
                "images",
                filename
            )

            with open(
                image_path,
                "wb"
            ) as file:

                file.write(image_bytes)

            image_number += 1


        # --------------------------------
        # 8. Add to report
        # --------------------------------

        report.append([
            page_number,
            extension,
            image_hash,
            status
        ])


# Close PDF
pdf.close()


# --------------------------------
# 9. Create CSV report
# --------------------------------

with open(
    "mapping_report.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Page",
        "Format",
        "Hash",
        "Status"
    ])

    writer.writerows(report)


# --------------------------------
# 10. Final result
# --------------------------------

print()
print("================================")
print("Extraction Completed!")
print("================================")

print("Unique images:", len(seen))

print(
    "Duplicate images:",
    len(report) - len(seen)
)

print("Images saved in: images")

print(
    "Report saved as: mapping_report.csv"
)