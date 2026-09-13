import markdown
from fpdf import FPDF

def main():
    # Read the markdown file and sanitize unicode characters
    with open("comparative_report.md", "r", encoding="utf-8") as f:
        md_text = f.read().replace("\u2014", "-").replace("\u2013", "-").replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")

    # Convert markdown to HTML with table support
    html_text = markdown.markdown(md_text, extensions=["tables"])

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=10)
    
    # fpdf2's write_html handles standard HTML tags well
    pdf.write_html(html_text)
    
    pdf.output("comparative_report.pdf")
    print("PDF generated successfully.")

if __name__ == "__main__":
    main()
