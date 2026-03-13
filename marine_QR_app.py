import base64
from io import BytesIO

import qrcode
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="Marine QR Generator", page_icon="🪖", layout="centered")

# ---------- Helper: background image ----------
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/webp;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    .block-container {{
        background-color: rgba(255,255,255,0.88);
        padding: 2rem;
        border-radius: 16px;
        margin-top: 2rem;
    }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

# Use your uploaded image file in the same repo/folder
add_bg_from_local("Marine.webp")

# ---------- Title ----------
st.title("Marine Corps QR Generator 🪖")

with st.expander("App Description"):
    st.write(
        """
        This app generates QR codes for URLs or text strings.
        You must first authenticate your allegiance before generating the code.

        POC: Brian Park, your_email@nps.edu
        """
    )

# ---------- Allegiance gate ----------
allegiance = st.text_input("Authenticate your allegiance first by typing Oorah!:")

# You can change this to 'Oorah!' if you want Marine-specific wording
required_phrase = "Oorah!"

if allegiance.strip() != required_phrase:
    st.warning(f"Access denied. Type exactly `{required_phrase}` to continue.")
    st.stop()

st.success("Allegiance authenticated. Oorah!")

# ---------- URL input ----------
text = st.text_input("Enter the URL or text to encode as QR Code:")

if text:
    qr_img = qrcode.make(text)
    img = qr_img._img

    st.write(f"QR Code generated for: {text}")
    st.image(img, caption="Generated QR Code", use_container_width=False)

    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download QR Code",
        data=byte_im,
        file_name="marine_qr_code.png",
        mime="image/png"
