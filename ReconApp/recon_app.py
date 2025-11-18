import streamlit as st
from pathlib import Path
import base64

# -------------------------------------------------------------------
# 1) Resolve the correct absolute path to the logo inside the app
# -------------------------------------------------------------------
LOGO_PATH = Path(__file__).parent / "static" / "logo.png"

# -------------------------------------------------------------------
# 2) Convert logo to base64 (this ALWAYS works, even on Streamlit Cloud)
# -------------------------------------------------------------------
def load_logo_base64(path: Path):
    if not path.exists():
        return None
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_b64 = load_logo_base64(LOGO_PATH)

# -------------------------------------------------------------------
# 3) Inject the logo + title header
# -------------------------------------------------------------------
if logo_b64:
    logo_html = f"""
        <img src="data:image/png;base64,{logo_b64}"
             style="width:130px; margin:0; padding:0;">
    """
else:
    logo_html = """
        <div style="color:red; font-weight:bold;">Logo not found</div>
    """

st.markdown(
    f"""
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;               /* VERY small distance (<0.5 cm) */
        margin-top:15px;
        margin-bottom:10px;
    ">
        {logo_html}
        <h1 style="
            margin:0;
            padding:0;
            font-size:42px;
            line-height:1;
            font-weight:700;
        ">
            Recon File Generator
        </h1>
    </div>

    <div style="height:25px;"></div> <!-- spacing before Step 1 -->
    """,
    unsafe_allow_html=True
)

