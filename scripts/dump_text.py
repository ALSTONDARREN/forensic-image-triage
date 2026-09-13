import docx

doc = docx.Document('Pereira_Alston_24850898.docx')

with open('dissertation_full_text.txt', 'w', encoding='utf-8') as f:
    for i, p in enumerate(doc.paragraphs):
        f.write(f'=== P{i} [{p.style.name}] ===\n')
        bolds = [repr(r.text) for r in p.runs if r.bold and r.text.strip()]
        if bolds:
            f.write(f'[BOLD]: {", ".join(bolds)}\n')
        f.write(p.text + '\n\n')

print('Wrote dissertation_full_text.txt successfully.')
