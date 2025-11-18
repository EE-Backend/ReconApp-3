import streamlit as st
import pandas as pd
from pathlib import Path
import base64
from io import BytesIO

# Import your backend function
from recon_engine import generate_reconciliation_file


# -----------------------------------------------------
# Streamlit page config
# -----------------------------------------------------
st.set_page_config(page_title="Recon File Generator", layout="wide")


# -----------------------------------------------------
# Load logo (base64)
# -----------------------------------------------------
BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "static" / "logo.png"   # ensure this file exists

def load_logo_as_base64(path: Path):
    if not path.exists():
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

logo_b64 = load_logo_as_base64(LOGO_PATH)


# -----------------------------------------------------
# Header (centered logo + title)
# -----------------------------------------------------
if logo_b64:
    logo_html = f"""
        <img src="data:image/png;base64,{logo_b64}" 
             style="width:110px;height:110px;object-fit:contain;margin:0;">
    """
else:
    # fallback if logo missing
    logo_html = """
        <div style="width:110px;height:110px;background:#999;border-radius:8px;"></div>
    """

# VERY tight spacing between logo & title using gap:8px
st.markdown(
    f"""
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:8px;
        margin-top:10px;
        margin-bottom:5px;
    ">
        {logo_html}
        <h1 style="margin:0; padding:0; font-size:40px; font-weight:700;">
            Recon File Generator
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# small visual spacer
st.write("")


# -----------------------------------------------------
# Step 1 — Upload Inputs
# -----------------------------------------------------
st.header("Step 1 — Upload Inputs")

trial_balance_file = st.file_uploader(
    "Upload Trial Balance file",
    type=["xlsx"],
    key="tb_upload"
)

entries_file = st.file_uploader(
    "Upload All Entries file",
    type=["xlsx"],
    key="entries_upload"
)

icp_code = st.text_input("Enter ICP Code", placeholder="Example: SKPVAB")


st.write("---")

# -----------------------------------------------------
# Step 2 — Generate
# -----------------------------------------------------
st.header("Step 2 — Generate Recon File")

if st.button("Generate Recon File", type="primary"):

    if not trial_balance_file or not entries_file or not icp_code.strip():
        st.error("❌ Please upload both files and enter an ICP code.")
        st.stop()

    with st.spinner("⏳ Generating reconciliation file..."):
        try:
            output_bytes = generate_reconciliation_file(
                trial_balance_file,
                entries_file,
                icp_code.strip().upper()
            )
        except Exception as e:
            st.error(f"❌ Error while generating file: {e}")
            raise

    st.success("✅ Reconciliation file generated successfully!")

    st.download_button(
        label="📥 Download Reconciliation Workbook",
        data=output_bytes,
        file_name="Reconciliation_Mapped.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.write("---")
st.caption("EE Internal Tool — Powered by Streamlit")


