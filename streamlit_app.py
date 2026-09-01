import os
import zipfile
import requests
import streamlit as st
from dotenv import load_dotenv

# ==========================================
# 1. Page Configuration & Custom CSS
# ==========================================
st.set_page_config(
    page_title="ShopMind AI | Intelligent Product Discovery",
    page_icon="🛍️",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .auth-container {
        max-width: 450px;
        margin: 40px auto;
        padding: 35px;
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .auth-title { color: #1e293b; font-size: 28px; font-weight: 800; }
    .auth-subtitle { color: #64748b; font-size: 14px; margin-bottom: 24px; }
    .shopmind-header {
        background-color: #0f172a;
        padding: 16px 32px;
        color: white;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
    }
    .shopmind-logo { color: #6366f1; font-size: 24px; font-weight: 800; }
    .shopmind-tagline { color: #94a3b8; font-size: 13px; border-left: 1px solid #334155; padding-left: 12px; }
    .welcome-card {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
        padding: 28px 32px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
    }
    .product-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease;
        height: 100%;
    }
    .product-card:hover { transform: translateY(-4px); }
    .product-img-container {
        width: 100%; height: 170px; overflow: hidden; border-radius: 10px; margin-bottom: 14px; background-color: #f1f5f9;
    }
    .product-img-container img { width: 100%; height: 100%; object-fit: cover; }
    .product-title { font-size: 15px; font-weight: 600; color: #1e293b; margin-bottom: 8px; }
    .product-rating { color: #f59e0b; font-size: 13px; font-weight: 600; }
    .product-price { color: #0f172a; font-size: 18px; font-weight: 700; margin-top: 6px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Authentication System
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
        <div class="auth-container">
            <div class="auth-title">ShopMind AI</div>
            <div class="auth-subtitle">Your Intelligent Shopping Assistant</div>
        </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        with st.form("signup_form"):
            full_name_input = st.text_input("Full Name", placeholder="Esraa Mahmoud")
            email_input = st.text_input("Email Address", placeholder="user@example.com")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            submit_button = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit_button:
                if email_input and password:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email_input
                    st.session_state.full_name = full_name_input if full_name_input.strip() else email_input.split('@')[0]
                    st.rerun()
                else:
                    st.warning("Please fill in all required fields.")
        
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px; margin-top: 15px;'>Already have an account? Sign in</p>", unsafe_allow_html=True)
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
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY missing!")
    st.stop()

# تهيئة المكتبة القديمة المسجلة في المشروع الأصلي
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ==========================================
# 4. Sidebar Navigation Menu
# ==========================================
user_display_name = st.session_state.get("full_name", st.session_state.user_email.split('@')[0])

with st.sidebar:
    st.markdown(f"### 👋 Hello, {user_display_name}")
    st.caption(f"📧 {st.session_state.user_email}")
    
    if st.button("Sign Out", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
        
    st.divider()
    st.markdown("#### Explore")
    st.markdown("🏠 **Home**")
    st.markdown("🔥 **Trending**")
    st.markdown("⭐ **Best Sellers**")
    st.markdown("🆕 **New Arrivals**")
    
    st.divider()
    st.markdown("#### Shop by Category")
    st.markdown("📱 **Electronics**")
    st.markdown("💻 **Computers**")
    st.markdown("🏠 **Home & Kitchen**")
    st.markdown("📚 **Books**")
    st.markdown("👕 **Fashion**")
    st.markdown("🎮 **Gaming**")

# ==========================================
# 5. Header & Banner
# ==========================================
st.markdown("""
<div class="shopmind-header">
    <div style="display: flex; align-items: center; gap: 12px;">
        <span class="shopmind-logo">🛍️ ShopMind AI</span>
        <span class="shopmind-tagline">Intelligent Product Discovery</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="welcome-card">
    <div style="font-size: 24px; font-weight: 700;">Welcome back, {user_display_name} 👋</div>
    <div style="color: #e0e7ff; font-size: 15px;">Discover products and ask our AI assistant questions about customer reviews.</div>
</div>
""", unsafe_allow_html=True)

st.text_input("Search Bar", placeholder="What are you looking for?", label_visibility="collapsed")
st.write("")

# ==========================================
# 6. Featured Products
# ==========================================
st.subheader("Featured Products")

products = [
    {"title": "Wireless Headphones", "rating": "⭐ 4.5", "price": "$89.99", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"},
    {"title": "Gaming Keyboard", "rating": "⭐ 4.7", "price": "$64.99", "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&q=80"},
    {"title": "Smart Watch", "rating": "⭐ 4.4", "price": "$79.99", "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80"},
]

cols = st.columns(3)
for idx, prod in enumerate(products):
    with cols[idx]:
        st.markdown(f"""
        <div class="product-card">
            <div class="product-img-container"><img src="{prod['image']}"/></div>
            <div class="product-title">{prod['title']}</div>
            <div class="product-rating">{prod['rating']}</div>
            <div class="product-price">{prod['price']}</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 7. Floating Chatbot Component
# ==========================================
st.write("")
st.divider()

with st.popover("💬 Chat with ShopMind AI Assistant", use_container_width=True):
    st.subheader("🤖 Ask ShopMind AI")
    st.caption("Ask questions about products and customer reviews.")
    
    query = st.text_input("Your Question:", placeholder="Is the PSU really 450w?")
    
    if st.button("Ask Assistant", type="primary"):
        if query:
            with st.spinner("Analyzing product reviews..."):
                try:
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
                    # توليد الإجابة بالمكتبة المستقرة الأصيلة
                    response = model.generate_content(prompt)
                    
                    st.markdown("#### 🤖 AI Answer")
                    st.success(response.text)
                    
                    with st.expander("🔎 View Retrieved Reviews"):
                        reviews_list = []
                        for i, item in enumerate(retrieved_chunks, start=1):
                            text = item["document"]
                            if "Answer:" in text:
                                text = text.split("Answer:")[-1].strip()
                            elif "Question:" in text:
                                text = text.split("?")[-1].replace("Answer:", "").strip()
                            reviews_list.append(f"**Review {i}:**\n{text}")
                        st.markdown("\n\n---\n\n".join(reviews_list))

                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
        else:
            st.warning("Please type a question first.")
