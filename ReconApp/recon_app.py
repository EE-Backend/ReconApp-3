import streamlit as st
import pandas as pd
from pathlib import Path
from recon_engine import generate_reconciliation_file

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(page_title="Recon File Generator", layout="wide")

# Base directory
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
LOGO_PATH = STATIC_DIR / "logo.png"

# ============================================
# CENTERED HEADER WITH LOGO + TITLE
# ============================================
st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center;">
""", unsafe_allow_html=True)

# Logo
if LOGO_PATH.exists():
    st.markdown(
        f"<img src='static/logo.png' style='width:130px; margin-bottom:5px;'>",
        unsafe_allow_html=True
    )
else:
    st.warning("Logo file not found in /static folder.")

# Title
st.markdown("""
    <h1 style="margin-top:0px; padding-top:0px;">
        Recon File Generator
    </h1>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Small spacing before UI
st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# ============================================
# STEP 1 — INPUTS
# ============================================
st.markdown("## Step 1 — Upload Inputs")
trial_balance_file = st.file_uploader(
    "Upload Trial Balance file",
    type=["xlsx"],
    key="trial_balance_upload"
)

entries_file = st.file_uploader(
    "Upload All Entries file",
    type=["xlsx"],
    key="entries_upload"
)

icp_code = st.text_input("Enter ICP Code", placeholder="Example: SKPVAB").strip()

st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

# ============================================
# STEP 2 — GENERATE
# ============================================
st.markdown("## Step 2 — Generate Recon File")

if st.button("Generate Recon File", type="primary"):

    if not trial_balance_file or not entries_file or not icp_code:
        st.error("Please upload both files and enter the ICP Code.")
        st.stop()

    with st.spinner("Generating file, please wait..."):
        try:
            output_bytes = generate_reconciliation_file(
                trial_balance_file,
                entries_file,
                icp_code.upper()
            )
        except Exception as e:
            st.error(f"❌ An error occurred:\n\n{e}")
            st.stop()

    st.success("✅ Reconciliation file generated successfully!")

    st.download_button(
        label="📥 Download Reconciliation Workbook",
        data=output_bytes,
        file_name="Reconciliation_Mapped.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.caption("European Energy — Internal Tool")

