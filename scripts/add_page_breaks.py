import os
from docx import Document
import win32com.client

docx_path = os.path.abspath('MSc_Dissertation_Draft.docx')
doc = Document(docx_path)

# Sections that absolutely must start on a brand new page in a thesis
major_sections = [
    "Abstract",
    "Declaration",
    "Acknowledgements",
    "Abbreviations",
    "List of Tables",
    "List of Figures",
    "Chapter 1:",
    "Chapter 2:",
    "Chapter 3:",
    "Chapter 4:",
    "Chapter 5:",
    "References",
    "Bibliography",
    "Appendix"
]

for p in doc.paragraphs:
    text = p.text.strip()
    
    # Check if the paragraph exactly matches or starts with one of our major section headings
    for section in major_sections:
        if text.startswith(section) and len(text) < 50: # Ensure it's a heading, not just a sentence starting with the word
            p.paragraph_format.page_break_before = True
            break # Move to next paragraph once a match is found

doc.save(docx_path)
print("Page breaks successfully added before all major sections.")

# Update the TOC again because the page numbers shifted
try:
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False
    
    doc_com = word.Documents.Open(docx_path)
    
    doc_com.Fields.Update()
    
    if doc_com.TablesOfContents.Count > 0:
        for toc in doc_com.TablesOfContents:
            toc.Update()
            
    doc_com.Save()
    doc_com.Close()
    word.Quit()
    print("Table of Contents successfully updated with new page numbers!")
except Exception as e:
    print(f"Error during COM automation: {e}")
    try:
        word.Quit()
    except:
        pass
