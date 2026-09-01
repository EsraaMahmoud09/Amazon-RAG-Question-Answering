import os
import zipfile
import requests
import streamlit as st
from dotenv import load_dotenv

# ==========================================
# 1. Page Configuration & Custom CSS
# ==========================================
st.set_page_config(
    page_title="ShopMind AI",
    page_icon="🛍️",
    layout="wide"
)

# ShopMind AI styling
st.markdown("""
<style>

    /* ==============================
       GLOBAL
    ============================== */

    .stApp {
        background-color: #f6f7fb;
    }

    .main {
        background-color: #f6f7fb;
    }

    /* ==============================
       TOP HEADER
       ============================== */

    .shop-header {
        background: linear-gradient(135deg, #182848, #4b6cb7);
        padding: 18px 28px;
        border-radius: 14px;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 25px;
        box-shadow: 0 5px 18px rgba(0,0,0,0.08);
    }

    .shop-logo {
        font-size: 27px;
        font-weight: 800;
        letter-spacing: 0.5px;
    }

    .shop-tagline {
        font-size: 14px;
        opacity: 0.9;
    }

    /* ==============================
       WELCOME SECTION
       ============================== */

    .welcome-box {
        background: white;
        padding: 28px;
        border-radius: 16px;
        margin-bottom: 25px;
        box-shadow: 0 3px 14px rgba(0,0,0,0.06);
    }

    .welcome-title {
        font-size: 28px;
        font-weight: 750;
        color: #182848;
        margin-bottom: 8px;
    }

    .welcome-text {
        color: #667085;
        font-size: 15px;
    }

    /* ==============================
       PRODUCT CARD
       ============================== */

    .product-card {
        background: white;
        padding: 15px;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.07);
        margin-bottom: 20px;
        min-height: 350px;
        transition: transform 0.2s ease;
    }

    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 7px 18px rgba(0,0,0,0.10);
    }

    .product-image {
        width: 100%;
        height: 190px;
        object-fit: contain;
        border-radius: 10px;
        background: #f8f9fc;
        margin-bottom: 12px;
    }

    .product-title {
        font-size: 16px;
        font-weight: 700;
        color: #1d2939;
        margin-top: 8px;
        min-height: 45px;
    }

    .product-rating {
        color: #667085;
        font-size: 13px;
        margin: 7px 0;
    }

    .product-price {
        color: #182848;
        font-size: 19px;
        font-weight: 800;
        margin-top: 5px;
    }

    /* ==============================
       AI SECTION
       ============================== */

    .ai-header {
        background: linear-gradient(135deg, #eef2ff, #f8f9ff);
        padding: 22px;
        border-radius: 15px;
        margin-top: 10px;
        margin-bottom: 15px;
        border: 1px solid #e4e7ec;
    }

    .ai-title {
        font-size: 21px;
        font-weight: 750;
        color: #182848;
    }

    .ai-subtitle {
        color: #667085;
        font-size: 14px;
        margin-top: 5px;
    }

    /* ==============================
       SIDEBAR
       ============================== */

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e4e7ec;
    }

    .sidebar-title {
        font-size: 20px;
        font-weight: 750;
        color: #182848;
    }

    .sidebar-section {
        font-size: 14px;
        font-weight: 700;
        color: #344054;
        margin-top: 18px;
        margin-bottom: 8px;
    }

    .sidebar-item {
        color: #667085;
        font-size: 14px;
        padding: 5px 0;
    }

    /* ==============================
       BUTTONS
       ============================== */

    .stButton > button {
        border-radius: 9px;
        border: none;
        font-weight: 650;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. Authentication System (Login Gate)
# ==========================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


if not st.session_state.authenticated:

    # Centered signup/login area
    left, center, right = st.columns([1, 2, 1])

    with center:

        st.markdown("""
        <div style="
            background:white;
            padding:35px;
            border-radius:18px;
            margin-top:60px;
            box-shadow:0 5px 25px rgba(0,0,0,0.08);
        ">
            <div style="
                text-align:center;
                font-size:30px;
                font-weight:800;
                color:#182848;
            ">
                🛍️ ShopMind AI
            </div>

            <div style="
                text-align:center;
                color:#667085;
                margin-top:8px;
                margin-bottom:25px;
            ">
                Your intelligent shopping assistant
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Create your account")

        with st.form("login_form"):

            name = st.text_input(
                "Full name",
                placeholder="Enter your name"
            )

            email = st.text_input(
                "Email address",
                placeholder="you@example.com"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password"
            )

            confirm_password = st.text_input(
                "Re-enter password",
                type="password",
                placeholder="Confirm your password"
            )

            submit_button = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

            if submit_button:

                if not name or not email or not password or not confirm_password:
                    st.warning("Please complete all fields.")

                elif password != confirm_password:
                    st.warning("Passwords do not match.")

                else:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.user_name = name
                    st.rerun()

        st.markdown(
            "<div style='text-align:center;color:#667085;margin-top:15px;'>"
            "Already have an account? Continue with your account"
            "</div>",
            unsafe_allow_html=True
        )

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

    response = requests.get(
        DB_URL,
        headers=headers,
        stream=True
    )

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

        st.error(
            f"❌ Failed to download database. "
            f"Status Code: {response.status_code}"
        )

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
# 4. Sidebar Navigation
# ==========================================

with st.sidebar:

    st.markdown(
        f"""
        <div class="sidebar-title">
            👋 Hello, {st.session_state.user_name}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(st.session_state.user_email)

    if st.button("Sign Out", use_container_width=True):

        st.session_state.authenticated = False
        st.rerun()

    st.divider()

    st.markdown(
        '<div class="sidebar-section">Explore</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">🏠 Home</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">🔥 Trending</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">⭐ Best Sellers</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">🆕 New Arrivals</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-section">Shop by Category</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">📱 Electronics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">💻 Computers</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">🏠 Home & Kitchen</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">📚 Books</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">👕 Fashion</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">🎮 Gaming</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-section">Your Account</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">👤 My Account</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">🛒 My Cart</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">❤️ Wishlist</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">⚙️ Settings</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-section">Help</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-item">❓ Customer Service</div>',
        unsafe_allow_html=True
    )


# ==========================================
# 5. Top Header
# ==========================================

st.markdown("""
<div class="shop-header">

    <div>
        <div class="shop-logo">
            🛍️ ShopMind AI
        </div>

        <div class="shop-tagline">
            Intelligent product discovery powered by AI
        </div>
    </div>

    <div style="font-size:14px;">
        🤖 AI Shopping Assistant
    </div>

</div>
""", unsafe_allow_html=True)


# ==========================================
# 6. Welcome Section
# ==========================================

st.markdown(f"""
<div class="welcome-box">

    <div class="welcome-title">
        Welcome back, {st.session_state.user_name} 👋
    </div>

    <div class="welcome-text">
        Discover products and ask our AI assistant
        questions about customer reviews.
    </div>

</div>
""", unsafe_allow_html=True)


# ==========================================
# 7. Mock Product Catalog
# ==========================================

st.markdown(
    "### ✨ Featured Products"
)

st.caption(
    "Explore some sample products before asking the AI assistant."
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown("""
    <div class="product-card">

        <img
            class="product-image"
            src="https://images.unsplash.com/photo-1546435770-a3e426bf472b"
        />

        <div class="product-title">
            Wireless Noise Cancelling Headphones
        </div>

        <div class="product-rating">
            ⭐ 4.5 / 5 · 2,341 reviews
        </div>

        <div class="product-price">
            $89.99
        </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown("""
    <div class="product-card">

        <img
            class="product-image"
            src="https://images.unsplash.com/photo-1587829741301-dc798b83add3"
        />

        <div class="product-title">
            Mechanical Gaming Keyboard
        </div>

        <div class="product-rating">
            ⭐ 4.7 / 5 · 1,892 reviews
        </div>

        <div class="product-price">
            $64.99
        </div>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown("""
    <div class="product-card">

        <img
            class="product-image"
            src="https://images.unsplash.com/photo-1523275335684-37898b6baf30"
        />

        <div class="product-title">
            Smart Fitness Watch
        </div>

        <div class="product-rating">
            ⭐ 4.4 / 5 · 3,120 reviews
        </div>

        <div class="product-price">
            $79.99
        </div>

    </div>
    """, unsafe_allow_html=True)


with col4:

    st.markdown("""
    <div class="product-card">

        <img
            class="product-image"
            src="https://images.unsplash.com/photo-1516035069371-29a1b244cc32"
        />

        <div class="product-title">
            Digital Mirrorless Camera
        </div>

        <div class="product-rating">
            ⭐ 4.6 / 5 · 987 reviews
        </div>

        <div class="product-price">
            $499.99
        </div>

    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 8. AI Shopping Assistant
# ==========================================

st.divider()

st.markdown("""
<div class="ai-header">

    <div class="ai-title">
        🤖 Ask ShopMind AI
    </div>

    <div class="ai-subtitle">
        Ask questions about products and customer reviews.
        The AI will answer using the available review data.
    </div>

</div>
""", unsafe_allow_html=True)


with st.expander(
    "💬 Open AI Product Assistant",
    expanded=True
):

    query = st.text_input(
        "What would you like to know?",
        key="chat_input",
        placeholder="e.g. Which product has the best customer reviews?"
    )

    if st.button(
        "Ask ShopMind AI",
        key="ask_btn",
        use_container_width=True
    ):

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

                st.subheader("AI Answer")

                st.success(response.text)

                with st.popover(
                    "View Retrieved Reviews"
                ):

                    reviews_list = []

                    for i, item in enumerate(
                        retrieved_chunks,
                        start=1
                    ):

                        text = item["document"]

                        if "Answer:" in text:

                            text = text.split(
                                "Answer:"
                            )[-1].strip()

                        elif "Question:" in text:

                            text = text.split(
                                "?"
                            )[-1].replace(
                                "Answer:",
                                ""
                            ).strip()

                        reviews_list.append(
                            f"**Review {i}:**\n{text}"
                        )

                    st.markdown(
                        "\n\n---\n\n".join(
                            reviews_list
                        )
                    )

        else:

            st.warning(
                "Please type a question first."
            )
```
