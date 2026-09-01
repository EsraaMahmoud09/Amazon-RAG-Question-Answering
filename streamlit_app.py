import os
import zipfile
import requests
import streamlit as st
from dotenv import load_dotenv

# ==========================================
# 1. Streamlit UI Configuration First
# ==========================================
st.set_page_config(
    page_title="Amazon RAG Assistant",
    page_icon="🛒",
    layout="wide"
)

# ==========================================
# 2. Download Database Automatically from GitHub Release
# ==========================================
DB_FOLDER = "chroma_db"
ZIP_FILE = "chroma_db.2.zip"
DB_URL = "https://github.com/EsraaMahmoud09/Amazon-RAG-Question-Answering/releases/download/v1.0.0/chroma_db.2.zip"

if not os.path.exists(DB_FOLDER):
    st.info("⏳ Downloading database for the first time, this may take a minute...")
    
    # Send request with User-Agent to prevent 403 Forbidden / 404 Errors
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(DB_URL, headers=headers, stream=True)
    
    if response.status_code == 200:
        with open(ZIP_FILE, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        # Extract contents
        with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
            zip_ref.extractall(".")
            
        # Remove zip after extraction
        if os.path.exists(ZIP_FILE):
            os.remove(ZIP_FILE)
            
        st.success("✅ Database downloaded and extracted successfully!")
    else:
        st.error(f"❌ Failed to download database. Status Code: {response.status_code}")
        st.stop()

# ==========================================
# 3. Import Search Utils & Gemini (After ensuring DB exists)
# ==========================================
from retrieve_utils import retrieve_context
from google import genai

# ==========================================
# 4. API Key & Client Setup
# ==========================================
load_dotenv()

# Read API Key from local .env or Streamlit Cloud Secrets
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY is missing! Please set it in Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# ==========================================
# 5. UI Content & User Input
# ==========================================
st.title("🛒 Amazon Product Question Answering Assistant")

st.write(
    """
    Ask any product-related question.
    The system retrieves relevant customer reviews
    and generates an answer using Gemini.
    """
)

query = st.text_input("Enter your product question:")

# ==========================================
# 6. Run RAG Pipeline
# ==========================================
if st.button("Get Answer"):
    if query:
        with st.spinner("Searching and generating answer..."):

            # Retrieve context and relevant chunks
            context, retrieved_chunks = retrieve_context(query)

            # Build Prompt
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

            # Generate answer using Gemini
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            answer = response.text

        # ==================================
        # 7. Display Results
        # ==================================
        st.subheader("Answer")
        st.success(answer)

        with st.expander("View Retrieved Documents"):
            # Combine all retrieved document texts into a single string
            combined_docs = "\n\n".join([item["document"] for item in retrieved_chunks])
            
            # Display the consolidated text inside the expander
            st.write(combined_docs)
    else:
        st.warning("Please enter a question first.")
