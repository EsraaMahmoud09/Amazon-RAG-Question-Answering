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

# Modern Navy / Indigo & Neutral Gray Theme Styling
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Login / Sign Up Card */
    .auth-container {
        max-width: 450px;
        margin: 40px auto;
        padding: 35px;
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .auth-title {
        color: #1e293b;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 4px;
    }
    .auth-subtitle {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 24px;
    }
    
    /* Top Navbar Header */
    .shopmind-header {
        background-color: #0f172a;
        padding: 16px 32px;
        color: white;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .shopmind-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .shopmind-logo {
        color: #6366f1;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    .shopmind-tagline {
        color: #94a3b8;
        font-size: 13px;
        border-left: 1px solid #334155;
        padding-left: 12px;
    }
    .header-actions {
        display: flex;
        gap: 20px;
        color: #cbd5e1;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Welcome Banner */
    .welcome-card {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
        padding: 28px 32px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.2);
    }
    .welcome-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .welcome-sub {
        color: #e0e7ff;
        font-size: 15px;
    }

    /* Product Cards Styling */
    .product-card {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .product-img-container {
        width: 100%;
        height: 170px;
        overflow: hidden;
        border-radius: 10px;
        margin-bottom: 14px;
        background-color: #f1f5f9;
    }
    .product-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .product-title {
        font-size: 15px;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 8px;
        line-height: 1.3;
        height: 40px;
        overflow: hidden;
    }
    .product-rating {
        color: #f59e0b;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .product-price {
        color: #0f172a;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .view-btn {
        background-color: #f1f5f9;
        color: #334155;
        text-align: center;
        padding: 8px 0;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        border: none;
    }

    /* AI Assistant Section */
    .ai-section {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 28px;
        margin-top: 32px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    .ai-header {
        font-size: 22px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
    }
    .ai-sub {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 20px;
    }
    .ai-response-card {
        background-color: #f8fafc;
        border-left: 4px solid #6366f1;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. Authentication System (Login / Create Account Gate)
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
            st.text_input("Full Name", placeholder="Esraa Mahmoud")
            email = st.text_input("Email Address", placeholder="user@example.com")
            password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            submit_button = st.form_submit_button("Create Account", use_container_width=True)
            
            if submit_button:
                if email and password:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.rerun()
                else:
                    st.warning("Please fill in all required fields.")
        
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 14px; margin-top: 15px;'>Already have an account? <a href='#' style='color: #6366f1; text-decoration: none; font-weight: 600;'>Sign in</a></p>", unsafe_allow_html=True)
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
# 4. Sidebar Navigation Menu
# ==========================================
user_display_name = st.session_state.user_email.split('@')[0].capitalize()

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
    
    st.divider()
    st.markdown("#### Your Account")
    st.markdown("👤 **My Account**")
    st.markdown("🛒 **My Cart**")
    st.markdown("❤️ **Wishlist**")
    st.markdown("⚙️ **Settings**")
    
    st.divider()
    st.markdown("#### Help")
    st.markdown("❓ **Customer Service**")

# ==========================================
# 5. Top Navbar Header
# ==========================================
st.markdown("""
<div class="shopmind-header">
    <div class="shopmind-brand">
        <span class="shopmind-logo">🛍️ ShopMind AI</span>
        <span class="shopmind-tagline">Intelligent Product Discovery</span>
    </div>
    <div class="header-actions">
        <span>🔍 Search</span>
        <span>👤 Account</span>
        <span>🛒 Cart (0)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. Welcome Section & Search Bar
# ==========================================
st.markdown(f"""
<div class="welcome-card">
    <div class="welcome-title">Welcome back, {user_display_name} 👋</div>
    <div class="welcome-sub">Discover products and ask our AI assistant questions about customer reviews.</div>
</div>
""", unsafe_allow_html=True)

st.text_input("Search Bar", placeholder="What are you looking for? (e.g. Wireless headphones, Gaming keyboard, Best camera...)", label_visibility="collapsed")

st.write("")

# ==========================================
# 7. Featured Products Grid (Mock Data)
# ==========================================
st.subheader("Featured Products")

products = [
    {
        "title": "Wireless Noise Cancelling Headphones",
        "rating": "⭐ 4.5 / 5 (2,341 reviews)",
        "price": "$89.99",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"
    },
    {
        "title": "Mechanical Gaming Keyboard",
        "rating": "⭐ 4.7 / 5 (1,892 reviews)",
        "price": "$64.99",
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&q=80"
    },
    {
        "title": "Smart Fitness Watch",
        "rating": "⭐ 4.4 / 5 (3,120 reviews)",
        "price": "$79.99",
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80"
    },
    {
        "title": "Digital Mirrorless Camera",
        "rating": "⭐ 4.6 / 5 (987 reviews)",
        "price": "$499.99",
        "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500&q=80"
    },
    {
        "title": "Wireless Bluetooth Speaker",
        "rating": "⭐ 4.3 / 5 (1,540 reviews)",
        "price": "$45.99",
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&q=80"
    },
    {
        "title": "Ergonomic Gaming Mouse",
        "rating": "⭐ 4.6 / 5 (2,120 reviews)",
        "price": "$39.99",
        "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&q=80"
    }
]

# Display 6 products in two rows of 3 columns
row1 = st.columns(3)
for idx, prod in enumerate(products[:3]):
    with row1[idx]:
        st.markdown(f"""
        <div class="product-card">
            <div class="product-img-container">
                <img src="{prod['image']}" alt="{prod['title']}"/>
            </div>
            <div class="product-title">{prod['title']}</div>
            <div class="product-rating">{prod['rating']}</div>
            <div class="product-price">{prod['price']}</div>
            <div class="view-btn">View Product</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

row2 = st.columns(3)
for idx, prod in enumerate(products[3:]):
    with row2[idx]:
        st.markdown(f"""
        <div class="product-card">
            <div class="product-img-container">
                <img src="{prod['image']}" alt="{prod['title']}"/>
            </div>
            <div class="product-title">{prod['title']}</div>
            <div class="product-rating">{prod['rating']}</div>
            <div class="product-price">{prod['price']}</div>
            <div class="view-btn">View Product</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 8. AI Shopping Assistant Section (RAG Integration)
# ==========================================
st.markdown("""
<div class="ai-section">
    <div class="ai-header">🤖 Ask ShopMind AI</div>
    <div class="ai-sub">Ask questions about products and customer reviews.</div>
</div>
""", unsafe_allow_html=True)

query = st.text_input("Input Query", placeholder="What would you like to know? (e.g., Which product has the best customer reviews?)", key="rag_input", label_visibility="collapsed")

if st.button("Ask ShopMind AI", key="ask_rag_btn", type="primary"):
    if query:
        with st.spinner("Analyzing product reviews with AI..."):
            # Unchanged RAG logic
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
            
            # Display Answer Card
            st.markdown("#### 🤖 AI Answer")
            st.info(response.text)
            
            # Display Retrieved Reviews Expander
            with st.expander("🔎 Sources / Retrieved Reviews"):
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
        st.warning("Please enter your question first.")
