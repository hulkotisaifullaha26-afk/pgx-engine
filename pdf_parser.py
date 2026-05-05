import pdfplumber
import os

# List of genes we know how to handle - from your CPIC dataset
KNOWN_GENES = [
    "CYP2D6", "CYP2C19", "CYP2C9", "CYP3A4", "CYP3A5",
    "SLCO1B1", "DPYD", "TPMT", "UGT1A1", "VKORC1",
    "CFTR", "G6PD", "HLA-A", "HLA-B", "IFNL3",
    "CYP2B6", "CYP4F2", "NUDT15", "RYR1", "CACNA1S"
]

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def find_genes_in_text(text):
    found_genes = []
    for gene in KNOWN_GENES:
        if gene in text.upper():
            found_genes.append(gene)
    return found_genes

def parse_pgx_report(pdf_path):
    print(f"Reading: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters of text")
    genes_found = find_genes_in_text(text)
    print(f"Genes detected: {genes_found}")
    return text, genes_found

# Test it
if __name__ == "__main__":
    pdf_path = input("Paste the full path to your PGx PDF and press Enter: ")
    if os.path.exists(pdf_path):
        text, genes = parse_pgx_report(pdf_path)
    else:
        print("File not found. Check the path and try again.")