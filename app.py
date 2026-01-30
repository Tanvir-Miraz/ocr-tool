import streamlit as st
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import io
import time
import random

# --- 1. PAGE CONFIG & CUSTOM CSS (The "Floating" Look) ---
st.set_page_config(page_title="Magic OCR Chef", page_icon="👨‍🍳", layout="centered")

# This CSS makes things look like they are floating on cards with shadows
st.markdown("""
    <style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(to right, #ece9e6, #ffffff);
    }
    /* Floating Card Style for the Main Container */
    .css-1y4p8pa {
        padding: 2rem;
        border-radius: 20px;
        background-color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    /* Success Button Styling */
    .stDownloadButton button {
        background-color: #4CAF50 !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. HEADER & ANIMATION ---
st.title("👨‍🍳 The OCR Kitchen")
st.markdown("### *We cook your PDF and serve fresh text!*")
st.write("---")

# --- 3. UPLOAD SECTION ---
uploaded_file = st.file_uploader("📂 Drop your ingredients (PDF) here:", type=["pdf"])

# --- 4. FUN STATUS MESSAGES ---
# The app will pick a random message from here based on progress
starter_msgs = [
    "🥬 Washing the vegetables...",
    "🥕 Peeling the cover page...",
    "🔪 Sharpening the digital knives...",
    "👨‍⚕️ The patient is on the surgery table..."
]

cooking_msgs = [
    "🔥 The book is cooking, please wait...",
    "🧂 Adding a pinch of salt to Page {page}...",
    "🧪 Extracting DNA from the font...",
    "🍳 Sautéing the paragraphs...",
    "🕵️ Scanning for secret codes...",
    "🧠 Performing brain surgery on the text..."
]

finishing_msgs = [
    "🍽️ Plating the results...",
    "🍒 Putting the cherry on top...",
    "🧹 Cleaning up the kitchen...",
    "🩹 Stitching the patient back together..."
]

# --- 5. THE LOGIC ---
if uploaded_file is not None:
    # A big, distinct start button
    if st.button("🚀 Start the Operation!", type="primary"):
        
        # Placeholders for dynamic updates
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        # Initial Fun Message
        status_text.info(f"✨ {random.choice(starter_msgs)}")
        time.sleep(1) # Dramatic pause

        # Read PDF
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = len(doc)
        full_text = ""

        # Processing Loop
        for i, page in enumerate(doc):
            # Update Progress
            percent = (i + 1) / total_pages
            progress_bar.progress(percent)
            
            # --- DYNAMIC FUN MESSAGES ---
            # Change message every 3 pages so it's not too frantic
            if i % 3 == 0:
                if percent < 0.8:
                    msg = random.choice(cooking_msgs).format(page=i+1)
                    status_text.warning(f"⏳ {msg}")
                else:
                    msg = random.choice(finishing_msgs)
                    status_text.info(f"✨ {msg}")

            # 1. Render Page (Fast)
            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            
            # 2. Extract Text
            text = pytesseract.image_to_string(image)
            full_text += f"--- PAGE {i+1} ---\n{text}\n\n"

        # Cleanup
        doc.close()
        progress_bar.empty()
        status_text.empty()
        
        # --- SUCCESS ---
        st.balloons()  # 🎈 ANIMATION!
        st.success("✅ Order Up! Your text is ready to be served.")
        
        # --- DOWNLOAD ---
        st.download_button(
            label="🥗 Download Your Fresh Text",
            data=full_text,
            file_name="served_text.txt",
            mime="text/plain"
        )
