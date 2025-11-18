import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path

from recon_engine import generate_reconciliation_file  # your backend function


# --- UI CONFIG --- #
st.set_page_config(
    page_title="Recon File Generator",
    layout="wide"
)

st.write("Upload the required files below and generate a standardized reconciliation workbook.")


# --- LOGO (optional but recommended) --- #
logo_path = Path("static/company_logo.png")

st.markdown("""
    <style>
        .logo-container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .logo-text {
            font-size: 2rem;
            font-weight: bold;
            margin-left: 15px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo-container">', unsafe_allow_html=True)

# Insert logo image if it exists
if logo_path.exists():
    st.image(str(logo_path), width=150)

# Insert title next to the logo
st.markdown('<div class="logo-text"> EE Recon File Generator</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


st.header("Step 1 — Upload Inputs")

# Upload Trial Balance
trial_balance_file = st.file_uploader(
    "Upload Trial Balance file",
    type=["xlsx"],
    key="trial_balance_upload"
)

# Upload Entries
entries_file = st.file_uploader(
    "Upload All Entries file",
    type=["xlsx"],
    key="entries_upload"
)

# ICP Code
icp_code = st.text_input("Enter ICP Code", placeholder="Example: SKPVAB")


st.write("---")
st.header("Step 2 — Generate Recon File")

generate_button = st.button("Generate Recon File", type="primary")

if generate_button:

    if not trial_balance_file or not entries_file or not icp_code.strip():
        st.error("❌ Please upload both files and enter an ICP code.")
        st.stop()

    with st.spinner("⏳ Generating reconciliation file..."):

        # Call your engine logic
        output_bytes = generate_reconciliation_file(
            trial_balance_file,
            entries_file,
            icp_code.strip().upper()
        )

    st.success("✅ Reconciliation file generated successfully!")

    st.download_button(
        label="📥 Download Reconciliation Workbook",
        data=output_bytes,
        file_name="Reconciliation_Mapped.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.write("---")
st.caption("EE Internal Tool — Powered by Streamlit")



