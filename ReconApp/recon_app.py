import streamlit as st
import pandas as pd
from io import BytesIO
from pathlib import Path
import base64

from recon_engine import generate_reconciliation_file


# ================================================================
# STREAMLIT PAGE CONFIG
# ================================================================
st.set_page_config(
    page_title="Recon File Generator",
    layout="wide"
)


# ================================================================
# LOAD & ENCODE LOGO (ALWAYS WORKS ON STREAMLIT CLOUD)
# ================================================================
LOGO_PATH = Path(__file__).parent / "static" / "logo.png"

def load_logo_base64(path: Path):
    if not path.exists():
        return None
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_b64 = load_logo_base64(LOGO_PATH)

if logo_b64:
    logo_html = f"""
        <img src="data:image/png;base64,{logo_b64}"
             style="width:130px; margin:0; padding:0;">
    """
else:
    logo_html = """
        <div style="color:red; font-weight:bold;">Logo not found</div>
    """


# ================================================================
# HEADER (CENTERED LOGO + TITLE, TIGHT SPACING)
# ================================================================
st.markdown(
    f"""
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;  
        margin-top:20px;
        margin-bottom:5px;
    ">
        {logo_html}
        <h1 style="
            margin:0;
            padding:0;
            font-size:42px;
            font-weight:700;
            line-height:1;
        ">
            Recon File Generator
        </h1>
    </div>

    <div style="height:25px;"></div>
    """,
    unsafe_allow_html=True
)


# ================================================================
# STEP 1 — INPUT SECTION
# ================================================================
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

# ================================================================
# STEP 2 — GENERATE FILE
# ================================================================
st.header("Step 2 — Generate Recon File")

generate_button = st.button("Generate Recon File", type="primary")

if generate_button:

    if not trial_balance_file or not entries_file or not icp_code.strip():
        st.error("❌ Please upload both files and enter an ICP code.")
        st.stop()

    with st.spinner("⏳ Generating reconciliation file..."):
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


# ================================================================
# FOOTER
# ================================================================
st.write("---")
st.caption("EE Internal Tool — Powered by Streamlit")
