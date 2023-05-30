# Francesco P.
# PDF to JPG converter

from pdf2image import convert_from_path
from sys import argv

DPI = 500

if __name__ == "__main__":
    pdf = argv[1]
    print("converting from pdf to image...")
    pages = convert_from_path(pdf, DPI)

    i = 1
    for page in pages:
        export_fname = pdf + " - page " + str(i) + ".jpg"
        print("exporting " + export_fname)
        page.save(export_fname, "JPEG")
        i = i + 1
