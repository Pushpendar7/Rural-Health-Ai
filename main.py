import streamlit as st
from google import genai
import PIL.Image

# --- 1. Page Configuration & UI Cleanup ---
st.set_page_config(page_title="Rural Health AI", page_icon="🏥")

# The "Strong" CSS to remove the floating GitHub/Streamlit badge
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Hides the floating "Hosted with Streamlit" / GitHub badge */
            div[data-testid="stStatusWidget"] {display: none !important;}
            .viewerBadge_container__1QSob {display: none !important;}
            .viewerBadge_link__1S137 {display: none !important;}
            [data-testid="stConnectionStatus"] {display: none !important;}
            
            /* Removes the toolbar at the top */
            [data-testid="stToolbar"] {display: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# ... (the rest of your code stays the same)

st.title(" Multilingual Rural Health Assistant")
st.markdown("---")

# --- 2. AI Client Setup ---
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def get_working_model():
    try:
        for m in client.models.list():
            if 'generateContent' in m.supported_actions and 'flash' in m.name:
                return m.name
    except:
        return "gemini-1.5-flash"

# --- 3. User Interface ---
target_lang = st.selectbox(
    "Select language for explanation:",
    ["English", "Hindi", "Telugu", "Tamil", "Marathi", "Bengali", "Gujarati"]
)

st.write("### 📸 Upload Prescription")
uploaded_file = st.file_uploader("Upload a photo (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = PIL.Image.open(uploaded_file)
    st.image(img, caption="Uploaded Prescription", use_container_width=True)
    
    if st.button("🚀 Analyze & Translate"):
        with st.spinner(f"Reading and translating to {target_lang}..."):
            try:
                model_id = get_working_model()
                
                prompt = f"""
                Identify the medicines in this image. 
                Explain them for a patient in a rural village.
                Provide the ENTIRE response in {target_lang}.
                
                Structure the response as:
                1. What is this medicine for? (Simple terms)
                2. How/When to take it?
                3. What kind of specialist doctor handles this?
                """
                
                response = client.models.generate_content(
                    model=model_id,
                    contents=[prompt, img]
                )
                
                st.success(f"Analysis complete in {target_lang}!")
                st.markdown(f"### 📋 Advice ({target_lang})")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("A Solution Challenge 2026 Prototype. Built with Google Gemini.")
