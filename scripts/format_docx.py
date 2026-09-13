import os
from docx import Document
import win32com.client
import time

docx_path = os.path.abspath('MSc_Dissertation_Draft.docx')

print("1. Updating Template Placeholders...")
doc = Document(docx_path)

for p in doc.paragraphs:
    if 'THE TITLE OF THE PROJECT' in p.text:
        p.text = p.text.replace('THE TITLE OF THE PROJECT', 'Evaluating Deterministic Computer Vision vs. Deep Learning for Digital Forensic Image Triage')
        # Center align it
        p.alignment = 1 
    if '2020' in p.text:
        p.text = p.text.replace('2020', '2026')
        p.alignment = 1

doc.save(docx_path)

print("2. Launching Microsoft Word in the background to update Table of Contents...")
try:
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False
    
    doc_com = word.Documents.Open(docx_path)
    
    # Force update all fields (Table of Contents, List of Figures, etc.)
    doc_com.Fields.Update()
    
    # Specifically update all Tables of Contents
    if doc_com.TablesOfContents.Count > 0:
        for toc in doc_com.TablesOfContents:
            toc.Update()
            
    doc_com.Save()
    doc_com.Close()
    word.Quit()
    print("Table of Contents successfully updated!")
except Exception as e:
    print(f"Error during COM automation: {e}")
    try:
        word.Quit()
    except:
        pass
