import streamlit as st
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import io
import time
import random

# --- 1. PAGE SETUP & DESIGN ---
st.set_page_config(page_title="Magic OCR Lab", page_icon="✨", layout="centered")

# Custom CSS for Background, Floating Buttons, and Fonts
st.markdown("""
    <style>
    /* 1. The Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* 2. Floating Card Container */
    .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 3rem !important;
        border-radius: 25px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        margin-top: 50px;
    }

    /* 3. Floating Button Style (Material Design) */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 18px;
        font-weight: bold;
        border-radius: 50px; /* Rounded pill shape */
        box-shadow: 0 10px 20px rgba(0,0,0,0.2); /* The floating shadow */
        transition: all 0.3s ease 0s;
        transform: translateY(0px);
    }

    /* Button Hover Effect */
    div.stButton > button:hover {
        transform: translateY(-5px); /* Moves up slightly */
        box-shadow: 0 15px 25px rgba(0,0,0,0.3); /* Shadow grows */
        color: #ffffff;
    }

    /* 4. Download Button (Green Theme) */
    div.stDownloadButton > button {
        background: linear-gradient(to right, #11998e 0%, #38ef7d 100%);
        color: white;
        border-radius: 50px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stDownloadButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 25px rgba(0,0,0,0.3);
    }

    /* Hide the default hamburger menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# --- 2. HEADER UI ---
st.title("✨ Magic OCR Lab")
st.markdown("### Upload your PDF and watch the magic happen.")
st.write("---")

# --- 3. UPLOAD SECTION ---
uploaded_file = st.file_uploader("📂 Drag & Drop your PDF file", type=["pdf"])

# --- 4. POP-UP MESSAGE LIBRARY ---
# These will appear as "Toasts" (Notifications)
pop_up_messages = [
    "👨‍⚕️ Patient is on the table...",
    "🔪 Making the first incision...",
    "🧠 Scanning neural pathways...",
    "🥬 Chopping the paragraphs...",
    "🔥 The server is heating up!",
    "🍳 Scrambling the pixels...",
    "🕵️ Decrypting ancient runes...",
    "🩹 Stitching the text back together...",
    "🍒 Adding the final garnish..."
]

# --- 5. MAIN LOGIC ---
if uploaded_file is not None:
    # Spacer to push button down slightly
    st.write("")
    
    # The Floating "Start" Button
    if st.button("🚀 ACTIVATE EXTRACTION"):
        
        # Initial Pop-up
        st.toast("🤖 System Online. Starting Engines...", icon="🚀")
        time.sleep(1)

        # Logic Setup
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = len(doc)
        full_text = ""
        
        # Progress Bar
        my_bar = st.progress(0)

        # Processing Loop
        for i, page in enumerate(doc):
            # Update Bar
            progress = (i + 1) / total_pages
            my_bar.progress(progress)
            
            # --- POP UP LOGIC ---
            # Show a funny toast every 20% progress or every 3 pages
            if i % 3 == 0 or i == 0:
                msg = random.choice(pop_up_messages)
                # st.toast creates the pop-up notification
                st.toast(msg, icon="⚡")
            
            # --- OCR WORK ---
            # Matrix=2.0 is roughly 200 DPI (High speed, Good quality)
            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            
            text = pytesseract.image_to_string(image)
            full_text += f"--- PAGE {i+1} ---\n{text}\n\n"

        # Cleanup
        doc.close()
        my_bar.empty() # Hide bar when done
        
        # Success Pop-up
        st.toast("✅ Extraction Complete!", icon="🎉")
        st.balloons()
        
        st.success("✨ Your text is ready!")

        # The Floating "Download" Button
        st.download_button(
            label="⬇️ DOWNLOAD RESULT",
            data=full_text,
            file_name="magic_extracted_text.txt",
            mime="text/plain"
        )
