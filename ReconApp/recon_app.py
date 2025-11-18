import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path
from recon_engine import generate_reconciliation_file


# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Recon File Generator",
    layout="wide"
)

st.title("📊 EE Recon File Generator")
st.write("Upload the required files below and generate a standardized reconciliation workbook.")


# -------------------------------------------------------
# STATIC FOLDER (internal files)
# -------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# LOGO FIX — your file is named logo.png
logo_path = STATIC_DIR / "logo.png"

if logo_path.exists():
    st.image(str(logo_path), width=180)
else:
    st.warning(f"⚠ Logo not found at: {logo_path}")


# -------------------------------------------------------
# INPUT SECTION
# -------------------------------------------------------
st.header("Step 1 — Upload Inputs")

# Upload Trial Balance
trial_balance_file = st.file_uploader(
    "Upload Trial Balance file",
    type=["xlsx"],
    key="trial_balance"
)

# Upload Entries
entries_file = st.file_uploader(
    "Upload All Entries file",
    type=["xlsx"],
    key="entries"
)

# ICP Code
icp_code = st.text_input("Enter ICP Code", placeholder="Example: SKPVAB")


st.write("---")
st.header("Step 2 — Generate Recon File")

generate_button = st.button("Generate Recon File", type="primary")


# -------------------------------------------------------
# PROCESSING
# -------------------------------------------------------
if generate_button:

    if not trial_balance_file or not entries_file or not icp_code.strip():
        st.error("❌ Please upload both files and enter an ICP code.")
        st.stop()

    with st.spinner("⏳ Generating reconciliation file..."):

        # Call engine logic
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

