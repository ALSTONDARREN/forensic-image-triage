import pypandoc
from docx import Document
from docxcompose.composer import Composer
import os

def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None

print("Preparing chapters...")
md_files = [
    'Chapter_1_Draft.md',
    'Chapter_2_Draft.md',
    'Chapter_3_Draft.md',
    'Chapter_4_Draft.md',
    'Chapter_5_Draft.md',
    'Chapter_6_Draft.md'
]

combined_md = ""
for file in md_files:
    with open(file, 'r', encoding='utf-8') as f:
        combined_md += f.read() + "\n\n"

with open('Full_Draft.md', 'w', encoding='utf-8') as f:
    f.write(combined_md)

print("Converting markdown to temporary docx...")
pypandoc.convert_file('Full_Draft.md', 'docx', outputfile='temp_chapters.docx')

print("Cleaning template dummy chapters...")
master = Document('report temp.docx')

# Find the start of Chapter 1 dummy text
start_idx = -1
for i, p in enumerate(master.paragraphs):
    if p.text.strip() == "Chapter 1":
        start_idx = i
        break

if start_idx != -1:
    # Delete everything from Chapter 1 onwards
    paragraphs_to_delete = master.paragraphs[start_idx:]
    for p in paragraphs_to_delete:
        delete_paragraph(p)

master.save('cleaned_temp.docx')

print("Merging fresh chapters into cleaned template...")
master = Document('cleaned_temp.docx')
# Add a page break before appending to ensure clean start
master.add_page_break()

composer = Composer(master)
doc_to_append = Document('temp_chapters.docx')
composer.append(doc_to_append)

try:
    composer.save('MSc_Dissertation_Draft.docx')
except PermissionError:
    print("PERMISSION ERROR: The file is currently open in Microsoft Word. Cannot overwrite.")
    
# Cleanup
os.remove('Full_Draft.md')
os.remove('temp_chapters.docx')
os.remove('cleaned_temp.docx')

print("Compilation successful! Dummy text removed and new chapters appended.")
