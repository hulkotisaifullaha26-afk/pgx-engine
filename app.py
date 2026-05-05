import streamlit as st
import tempfile
import os
from pdf_parser import parse_pgx_report
from cpic_lookup import lookup_genes
from interpreter import interpret_pgx_results

# --- Page config ---
st.set_page_config(
    page_title="PGx Interpreter",
    page_icon="🧬",
    layout="centered"
)

# --- Header ---
st.title("🧬 PGx Report Interpreter")
st.subheader("Upload your pharmacogenomics report and get a plain-language explanation")
st.markdown("---")

# --- CPIC data path (hardcoded for now) ---
CPIC_PATH =r"C:\Users\hulko\Downloads\cpic-genes-drugs.tsv"
# --- File uploader ---
uploaded_file = st.file_uploader(
    "Upload your PGx PDF report",
    type=["pdf"],
    help="Supported formats: 23andMe, Invitae, GeneDx, MedGenome, and most standard PGx reports"
)

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")

    if st.button("🔍 Analyse My Report", use_container_width=True):

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        try:
            # Step 1 - Parse PDF
            with st.spinner("Reading your report..."):
                text, genes = parse_pgx_report(tmp_path)

            if not genes:
                st.error("No recognisable genes found in this PDF. Make sure it is a pharmacogenomics report.")
            else:
                # Show detected genes
                st.markdown("### Genes detected in your report")
                cols = st.columns(len(genes))
                for i, gene in enumerate(genes):
                    cols[i].metric(label="Gene", value=gene)

                # Step 2 - CPIC lookup
                with st.spinner("Looking up clinical guidelines..."):
                    gene_drug_pairs = lookup_genes(genes, CPIC_PATH)

                st.markdown(f"**{len(gene_drug_pairs)} gene-drug relationships found**")

                # Step 3 - AI interpretation
                with st.spinner("Generating your personalised interpretation..."):
                    report = interpret_pgx_results(gene_drug_pairs)

                st.markdown("---")
                st.markdown("### Your Personalised Report")
                st.markdown(report)

                st.markdown("---")
                st.download_button(
                    label="📄 Download Report",
                    data=report,
                    file_name="pgx_interpretation.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        finally:
            os.unlink(tmp_path)

else:
    st.info("👆 Upload your PDF above to get started. Your data is never stored.")

st.caption("PGx Interpreter uses CPIC clinical guidelines and AI to help you understand your pharmacogenomics results. This is not medical advice.")