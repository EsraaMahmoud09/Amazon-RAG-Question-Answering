import os
import zipfile
import gdown
import streamlit as st
from dotenv import load_dotenv

# ==========================================
# 1. Download Database Automatically on First Run
# ==========================================
DB_FOLDER = "chroma_db"
ZIP_FILE = "chroma_db.zip"

# ⬇️ Replace the text below with your File ID from your Google Drive link
GDRIVE_FILE_ID = "1W69NkpHQTLSSDNY-IvGgLLFPOWEEl6Ia"
url = f'https://drive.google.com/uc?id={1W69NkpHQTLSSDNY-IvGgLLFPOWEEl6Ia}'

if not os.path.exists(DB_FOLDER):
    st.info("⏳ Downloading database for the first time, this may take a minute...")
    url = f'https://drive.google.com/uc?id={1W69NkpHQTlSSDNY-IvGgLLfPOWEEl6Ia}'
    
    # Download the file
    gdown.download(url, ZIP_FILE, quiet=False)
    
    # Extract zip file
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(".")
    
    # Remove downloaded zip file to save storage space
    if os.path.exists(ZIP_FILE):
        os.remove(ZIP_FILE)
        
    st.success("✅ Database downloaded and extracted successfully!")

# ==========================================
# 2. Import Search Utils & Gemini (After ensuring DB exists)
# ==========================================
from retrieve_utils import retrieve_context
from google import genai

# ==========================================
# 3. API Key & Client Setup
# ==========================================
load_dotenv()

# Read API Key from local .env or Streamlit Cloud Secrets
api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# ==========================================
# 4. Streamlit UI Configuration
# ==========================================
st.set_page_config(
    page_title="Amazon RAG Assistant",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Amazon Product Question Answering Assistant")

st.write(
    """
    Ask any product-related question.
    The system retrieves relevant customer reviews
    and generates an answer using Gemini.
    """
)

# ==========================================
# 5. User Input
# ==========================================
query = st.text_input("Enter your product question:")

# ==========================================
# 6. Run RAG Pipeline
# ==========================================
if st.button("Get Answer"):
    if query:
        with st.spinner("Searching and generating answer..."):

            # Retrieve context and relevant chunks from vector store
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
            for i, item in enumerate(retrieved_chunks, start=1):
                st.write(f"### Document {i}")
                st.write(item["document"])
    else:
        st.warning("Please enter a question first.")
