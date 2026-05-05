import pandas as pd

def load_cpic_data(csv_path):
    try:
        df = pd.read_csv(csv_path, sep='\t', on_bad_lines='skip')
    except:
        df = pd.read_csv(csv_path, on_bad_lines='skip')
    print(f"Loaded {len(df)} rows from CPIC dataset")
    print(f"Columns: {list(df.columns)}")
    return df

def get_drugs_for_gene(df, gene_name):
    # Filter rows where Gene column matches
    matches = df[df['Gene'].str.upper() == gene_name.upper()]
    if matches.empty:
        return []
    # Return list of dicts with drug and CPIC level
    results = []
    for _, row in matches.iterrows():
        results.append({
            'drug': row['Drug'],
            'cpic_level': row['CPIC Level'],
            'gene': gene_name
        })
    return results

def lookup_genes(genes_found, cpic_csv_path):
    df = load_cpic_data(cpic_csv_path)
    all_matches = []
    for gene in genes_found:
        matches = get_drugs_for_gene(df, gene)
        if matches:
            print(f"\n{gene} — {len(matches)} drug(s) found:")
            for m in matches:
                print(f"  {m['drug']} (CPIC Level: {m['cpic_level']})")
            all_matches.extend(matches)
        else:
            print(f"\n{gene} — no matches in CPIC dataset")
    return all_matches

# Test it
if __name__ == "__main__":
    genes = ['CYP2C19', 'SLCO1B1', 'DPYD']
    cpic_path = input("Paste the full path to your CPIC CSV file and press Enter: ")
    results = lookup_genes(genes, cpic_path)
    print(f"\nTotal gene-drug pairs found: {len(results)}")