from pdf_parser import parse_pgx_report
from cpic_lookup import lookup_genes
from interpreter import interpret_pgx_results

# Step 1 — set your file paths
pdf_path = r"C:\Users\hulko\Downloads\23andMe-Pharmacogenetics-Summary-Report.pdf"
cpic_path = r"C:\Users\hulko\Downloads\cpic-genes-drugs.tsv"
text, genes = parse_pgx_report(pdf_path)
gene_drug_pairs = lookup_genes(genes, cpic_path)
# Step 3
report = interpret_pgx_results(gene_drug_pairs)
print("\n--- FINAL REPORT ---\n")
print(report)