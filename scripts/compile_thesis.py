import pypandoc
from docx import Document
from docxcompose.composer import Composer
import os

# 1. Ensure pandoc is downloaded locally
print("Downloading pandoc...")
pypandoc.download_pandoc()

# 2. Combine Markdown files
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

# 3. Convert combined Markdown to a temporary docx
print("Converting markdown to temporary docx...")
pypandoc.convert_file('Full_Draft.md', 'docx', outputfile='temp_chapters.docx')

# 4. Merge into the university template
print("Merging into report temp.docx...")
master = Document('report temp.docx')
# Optional: Add a page break at the end of the template before appending chapters
master.add_page_break()

composer = Composer(master)
doc_to_append = Document('temp_chapters.docx')
composer.append(doc_to_append)

composer.save('MSc_Dissertation_Draft.docx')

# 5. Cleanup
os.remove('Full_Draft.md')
os.remove('temp_chapters.docx')

print("Compilation successful! Saved to MSc_Dissertation_Draft.docx")
