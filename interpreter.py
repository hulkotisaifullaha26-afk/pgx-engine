import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def interpret_pgx_results(gene_drug_pairs):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    summary = ""
    for pair in gene_drug_pairs:
        summary += f"- Gene: {pair['gene']} | Drug: {pair['drug']} | Evidence Level: {pair['cpic_level']}\n"

    prompt = f"""You are a clinical pharmacogenomics expert helping a patient understand their genetic test results.

A patient's PGx report has revealed the following gene-drug relationships based on CPIC guidelines:

{summary}

Write a clear, plain-language interpretation for this patient. Structure your response as follows:

1. OVERVIEW (2-3 sentences summarising what their results mean overall)

2. FOR EACH GENE, explain:
   - What this gene does in the body
   - Which of their medications are affected (focus on Level A evidence only)
   - What the practical implication is (e.g. may need dose adjustment, alternative drug recommended)

3. IMPORTANT NOTE: End with a clear disclaimer that this is for informational purposes only and they must consult their doctor or pharmacist before making any changes to their medications.

Use simple language. Avoid jargon. Write as if explaining to an educated non-medical person."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content

# Test it
if __name__ == "__main__":
    test_pairs = [
        {'gene': 'CYP2C19', 'drug': 'clopidogrel', 'cpic_level': 'A'},
        {'gene': 'CYP2C19', 'drug': 'omeprazole', 'cpic_level': 'A'},
        {'gene': 'CYP2C19', 'drug': 'escitalopram', 'cpic_level': 'A'},
        {'gene': 'SLCO1B1', 'drug': 'simvastatin', 'cpic_level': 'A'},
        {'gene': 'SLCO1B1', 'drug': 'atorvastatin', 'cpic_level': 'A'},
        {'gene': 'DPYD', 'drug': 'fluorouracil', 'cpic_level': 'A'},
        {'gene': 'DPYD', 'drug': 'capecitabine', 'cpic_level': 'A'},
    ]

    print("Sending to AI for interpretation...\n")
    result = interpret_pgx_results(test_pairs)
    print(result)