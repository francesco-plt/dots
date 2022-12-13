#!/opt/homebrew/bin/python3
from os.path import isfile, expanduser
from os import remove
from pikepdf import Pdf


# create a list with file names
homepath = expanduser("~")
old_slides = expanduser("~") + '/OneDrive - Politecnico di Milano/Courses/Algebra and Mathematical Logic [Luca Mauri]/Slides.pdf'
new_slides = expanduser("~") + '/Downloads/Slides.pdf'
merged_slides = expanduser("~") + '/OneDrive - Politecnico di Milano/Courses/Algebra and Mathematical Logic [Luca Mauri]/Slides_merge.pdf'

# check for file existence
if not isfile(old_slides):
    print('File not found: ' + old_slides)
    exit(1)
if not isfile(new_slides):
    print('File not found: ' + new_slides)
    exit(1)
if isfile(merged_slides):
    remove(merged_slides)


old_pdf = Pdf.open(old_slides)
new_pdf = Pdf.open(new_slides)
merged_pdf = Pdf.new()
# count pages in old slides
oldcount = len(old_pdf.pages)
newcount = len(new_pdf.pages)
# we want to add the new slides at the end of the old ones
# and write them to a new file, which is merged_slides
print("generating merged slides...")
for i in range(0, oldcount):
    merged_pdf.pages.append(old_pdf.pages[i])
for i in range(oldcount, newcount):
    merged_pdf.pages.append(new_pdf.pages[i])
print("writing merged slides...")
merged_pdf.save(merged_slides)
print("done!")
