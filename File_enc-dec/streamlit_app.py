'''This is a Streamlit app for file encryption and decryption.

This app allows users to upload a text file, choose to encrypt or decrypt it using a Caesar cipher,
specify the shift value, and then download the processed file.

It uses the Backend Logic form the file_encryptor.py module.

To run this please make sure to download Streamlit app in your computer on in you virtual environment.

`pip install streamlit`

Then run the app with: `streamlit run streamlit_app.py`

'''

import io
from pathlib import Path
import streamlit as st
from file_encryptor import process_file, DEFAULT_SHIFT  # reuse your backend functions

st.set_page_config(page_title="File Encryptor", page_icon="🔐", layout="centered")
st.title("🔐 File Encryptor/Decryptor")
st.write("Upload a text file, choose encryption or decryption, and download the result.")

# UI elements
mode = st.radio("Mode", ["Encrypt", "Decrypt"], horizontal=True)
shift = st.number_input("Shift value", value=DEFAULT_SHIFT, step=1)
uploaded = st.file_uploader("Upload text file", type=["txt", "md", "csv", "log"])
process = st.button("Run")

if process:
    if uploaded is None:
        st.warning("Please upload a file first.")
    else:
        input_path = Path("temp_input.txt")
        output_path = Path("temp_output.txt")
        input_path.write_bytes(uploaded.read())

        try:
            # Use your backend's process_file()
            result_path = process_file(
                input_path=input_path,
                output_path=output_path,
                shift=shift,
                encrypt=(mode == "Encrypt")
            )
            result_data = result_path.read_bytes()
            st.success(f"✅ {mode}ion complete!")

            st.download_button(
                label="⬇️ Download result",
                data=io.BytesIO(result_data),
                file_name=f"{uploaded.name.split('.')[0]}_{mode.lower()}.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Error: {e}")
