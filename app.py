import streamlit as st
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import io

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="My OCR Scanner", page_icon="📄")

st.title("📄 PDF to Text Converter")
st.write("Upload a PDF, click the button, and get the text.")

# --- 2. THE UPLOAD BUTTON ---
uploaded_file = st.file_uploader("Choose your PDF file", type=["pdf"])

# --- 3. THE MAGIC BUTTON ---
if uploaded_file is not None:
    if st.button("🚀 Start Scanning"):
        
        st.info("Processing... please wait.")
        my_bar = st.progress(0)
        
        # Read the PDF file
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = len(doc)
        
        full_text = ""
        
        # Loop through pages
        for i, page in enumerate(doc):
            # Update Progress Bar
            progress = (i + 1) / total_pages
            my_bar.progress(progress)
            
            # Render page to image (Fast 150 DPI)
            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            
            # Extract Text
            text = pytesseract.image_to_string(image)
            full_text += f"--- PAGE {i+1} ---\n{text}\n\n"
            
        doc.close()
        my_bar.empty() # Clear progress bar
        
        st.success(f"✅ Done! Extracted {total_pages} pages.")

        # --- 4. DOWNLOAD BUTTON ---
        st.download_button(
            label="⬇️ Download Text File",
            data=full_text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )
