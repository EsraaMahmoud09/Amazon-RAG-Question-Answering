import os
import zipfile
import requests
import streamlit as st
from dotenv import load_dotenv

# ==========================================
# 1. Page Configuration & Custom CSS
# ==========================================
st.set_page_config(
    page_title="Amazon Shopping & AI Assistant",
    page_icon="🛒",
    layout="wide"
)

# Amazon-inspired styling
st.markdown("""
<style>
    /* Main Background & Fonts */
    .main { background-color: #eaeded; }
    
    /* Top Navbar Header */
    .amazon-header {
        background-color: #131921;
        padding: 15px 20px;
        color: white;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .amazon-logo {
        color: #ff9900;
        font-size: 26px;
        font-weight: bold;
    }
    
    /* Product Card Styling */
    .product-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .product-title {
        font-size: 16px;
        font-weight: bold;
        color: #0f1111;
        margin-top: 10px;
    }
    .product-price {
        color: #B12704;
        font-size: 18px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Authentication System (Login Gate)
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔑 Sign-in to Amazon AI Assistant")
    with st.form("login_form"):
        email = st.text_input("Enter your email address:")
        password = st.text_input("Enter your password:", type="password")
        submit_button = st.form_submit_button("Continue")
        
        if submit_button:
            if email and password:
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.rerun()
            else:
                st.warning("Please enter both email and password.")
    st.stop()

# ==========================================
# 3. Database Auto-Download
# ==========================================
DB_FOLDER = "chroma_db"
ZIP_FILE = "chroma_db.2.zip"
DB_URL = "https://github.com/EsraaMahmoud09/Amazon-RAG-Question-Answering/releases/download/v1.0.0/chroma_db.2.zip"

if not os.path.exists(DB_FOLDER):
    st.info("⏳ Downloading database for the first time...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(DB_URL, headers=headers, stream=True)
    
    if response.status_code == 200:
        with open(ZIP_FILE, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
            zip_ref.extractall(".")
        if os.path.exists(ZIP_FILE):
            os.remove(ZIP_FILE)
        st.success("✅ Database downloaded!")
    else:
        st.error(f"❌ Failed to download database. Status Code: {response.status_code}")
        st.stop()

from retrieve_utils import retrieve_context
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing!")
    st.stop()

client = genai.Client(api_key=api_key)

# ==========================================
# 4. Amazon Sidebar Navigation Menu
# ==========================================
with st.sidebar:
    st.markdown(f"### 👤 Hello, {st.session_state.user_email.split('@')[0]}")
    if st.button("Sign Out"):
        st.session_state.authenticated = False
        st.rerun()
        
    st.divider()
    st.subheader("Trending")
    st.write("• Best Sellers")
    st.write("• New Releases")
    
    st.divider()
    st.subheader("Shop by Category")
    st.write("• Mobiles, Tablets & Accessories")
    st.write("• Computers & Office Supplies")
    st.write("• TVs & Electronics")
    st.write("• Women's Fashion")
    
    st.divider()
    st.subheader("Help & Settings")
    st.write("• Your Account")
    st.write("• Customer Service")

# ==========================================
# 5. Top Header & Mock Product Catalog
# ==========================================
st.markdown("""
<div class="amazon-header">
    <div class="amazon-logo">amazon.eg</div>
    <div>Deals & finds for your product search</div>
</div>
""", unsafe_allow_html=True)

# Product Grid Display
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="product-card">
        <img src="https://via.placeholder.com/200x150?text=PC+Power+Supply" width="100%"/>
        <div class="product-title">450W Gaming PSU</div>
        <div class="product-price">1,299 EGP</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="product-card">
        <img src="https://via.placeholder.com/200x150?text=Brake+Pads" width="100%"/>
        <div class="product-title">Front & Rear Brake Pads</div>
        <div class="product-price">850 EGP</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="product-card">
        <img src="https://via.placeholder.com/200x150?text=Electronics" width="100%"/>
        <div class="product-title">Consumer Electronics</div>
        <div class="product-price">2,499 EGP</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 6. Floating RAG Chatbot Drawer
# ==========================================
st.divider()

with st.expander("💬 Chat with Amazon RAG Assistant (Ask Product Questions)", expanded=True):
    query = st.text_input("Ask any product question based on reviews:", key="chat_input")
    
    if st.button("Ask Assistant", key="ask_btn"):
        if query:
            with st.spinner("Analyzing product reviews..."):
                context, retrieved_chunks = retrieve_context(query)
                
                prompt = f"""
You are an Amazon Product Question Answering Assistant.

Answer the customer question using ONLY the provided context.

Rules:
- Give a direct answer.
- Rewrite naturally.
- Do not invent information.
- If reviews conflict, explain the difference.
- If information is missing, say:
"I don't have enough information from the available product reviews."

Context:
{context}

Question:
{query}

Answer:
"""
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                st.subheader("Assistant Answer:")
                st.success(response.text)
                
                with st.popover("View Retrieved Reviews"):
                    reviews_list = []
                    for i, item in enumerate(retrieved_chunks, start=1):
                        text = item["document"]
                        if "Answer:" in text:
                            text = text.split("Answer:")[-1].strip()
                        elif "Question:" in text:
                            text = text.split("?")[-1].replace("Answer:", "").strip()
                        reviews_list.append(f"**Review {i}:**\n{text}")
                    st.markdown("\n\n---\n\n".join(reviews_list))
        else:
            st.warning("Please type a question first.")
