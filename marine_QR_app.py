import base64
from io import BytesIO

import qrcode
import streamlit as st

st.set_page_config(page_title="Marine QR Generator", page_icon="🪖", layout="centered")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    file_ext = image_file.split(".")[-1].lower()

    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/{file_ext};base64,{encoded}");
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

add_bg_from_local("Marine.webp")

st.title("Marine Corps QR Generator 🪖")

with st.expander("App Description"):
    st.write("""
    This app generates QR codes for URLs or text strings.
    You must first authenticate your allegiance before generating the code.

    POC: Brian Park, your_email@nps.edu
    """)

allegiance = st.text_input("Authenticate your allegiance first by typing Oorah!:")

required_phrase = "Oorah!"

if allegiance.strip() != required_phrase:
    st.warning(f"Access denied. Type exactly `{required_phrase}` to continue.")
    st.stop()

st.success("Allegiance authenticated. Oorah!")

text = st.text_input("Enter the URL or text to encode as QR Code:")

if text:
    img = qrcode.make(text)

    st.write(f"QR Code generated for: {text}")
    st.image(img, caption="Generated QR Code")

    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download QR Code",
        data=byte_im,
        file_name="marine_qr_code.png",
        mime="image/png"
    )
