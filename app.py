import streamlit as st
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import io
import time
import random
import base64

# --- 1. PAGE CONFIG & LOGO LOADING ---
# We load the image first so we can use it in the browser tab icon
try:
    logo_img = Image.open("logo.png")
    st.set_page_config(page_title="Ultra OCR", page_icon=logo_img, layout="centered")
except:
    # Fallback if logo.png is missing from your GitHub
    st.set_page_config(page_title="Ultra OCR", page_icon="🔮", layout="centered")

# --- 2. ADVANCED CSS (ANIMATIONS & GLASSMORPHISM) ---
st.markdown("""
    <style>
    /* ANIMATED BACKGROUND */
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    /* GLASS CONTAINER */
    .block-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* CENTER POP-UP NOTIFICATION (THE HUD) */
    .center-hud {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0, 0, 0, 0.85);
        color: white;
        padding: 30px 50px;
        border-radius: 25px;
        text-align: center;
        z-index: 999999;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        backdrop-filter: blur(5px);
        border: 2px solid rgba(255,255,255,0.1);
        animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    @keyframes popIn {
        from { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }
        to { transform: translate(-50%, -50%) scale(1); opacity: 1; }
    }

    /* FLOATING BUTTONS - Change to Red Theme to match logo */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #F03E3E 0%, #8b0000 100%);
        color: white;
        border: none;
        padding: 18px 32px;
        font-size: 20px;
        border-radius: 50px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 30px rgba(0,0,0,0.4);
        color: #fff;
    }

    /* PROGRESS BAR COLOR */
    .stProgress > div > div > div > div {
        background-color: #F03E3E;
    }
    
    /* HIDE DEFAULT STREAMLIT MENU */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# --- 3. HELPER FUNCTION FOR CENTER POP-UP ---
def show_hud_message(placeholder, emoji, message, subtext=""):
    placeholder.markdown(
        f"""
        <div class="center-hud">
            <div style="font-size: 60px; margin-bottom: 10px;">{emoji}</div>
            <div>{message}</div>
            <div style="font-size: 16px; color: #ccc; margin-top: 5px;">{subtext}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- 4. APP LOGIC ---

# DISPLAY LOGO IN SIDEBAR AND MAIN HEADER
if 'logo_img' in locals():
    st.sidebar.image(logo_img, width=150)
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(logo_img, width=80)
    with col2:
        st.title("Crystal Clear OCR")
else:
    st.title("OCR KITCHEN👨‍🍳")

st.markdown("### *Transforming images into words...*")

uploaded_file = st.file_uploader(" ", type=["pdf"])

# Placeholder for the Center HUD (Heads-Up Display)
hud_placeholder = st.empty()

if uploaded_file is not None:
    st.write("---")
    
    if st.button("🚀 ACTIVATE EXTRACTION"):
        
        # 1. INITIAL ANIMATION
        show_hud_message(hud_placeholder, "⚡", "INITIALIZING", "Waking up the AI...")
        time.sleep(1.5)
        
        # Setup
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        total_pages = len(doc)
        full_text = ""
        
        my_bar = st.progress(0)
        
        # FUN MESSAGES LIST
        loading_steps = [
            ("🥬", "PREPARING INGREDIENTS", "Slicing PDF pages..."),
            ("🔦", "SCANNING PIXELS", "Searching for ink..."),
            ("🧠", "AI THINKING", "Deciphering handwriting..."),
            ("👨‍⚕️", "SURGERY IN PROGRESS", "Extracting text DNA..."),
            ("🔥", "HEATING UP", "The GPU is cooking!"),
            ("💎", "POLISHING", "Cleaning up artifacts..."),
        ]

        # 2. PROCESSING LOOP
        for i, page in enumerate(doc):
            # Update Bar
            progress = (i + 1) / total_pages
            my_bar.progress(progress)
            
            # SHOW CENTER POP-UP (Every few pages or first page)
            if i % 2 == 0 or i == 0:
                # Pick a random lively message
                emoji, main_text, sub_text = random.choice(loading_steps)
                real_sub_text = f"{sub_text} (Page {i+1})"
                show_hud_message(hud_placeholder, emoji, main_text, real_sub_text)
                
                time.sleep(0.3)

            # OCR Extraction
            pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            text = pytesseract.image_to_string(image)
            full_text += f"--- PAGE {i+1} ---\n{text}\n\n"

        # 3. FINISH ANIMATION
        doc.close()
        my_bar.empty()
        
        # Success HUD
        show_hud_message(hud_placeholder, "🎉", "MISSION COMPLETE", "Your text is served.")
        st.balloons()
        time.sleep(2)
        hud_placeholder.empty()

        # 4. DOWNLOAD CARD
        st.success("✅ Extraction successful!")
        
        st.download_button(
            label="⬇️ DOWNLOAD TEXT FILE",
            data=full_text,
            file_name="crystal_extracted.txt",
            mime="text/plain"
        )
