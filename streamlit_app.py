import streamlit as st
import os

from dotenv import load_dotenv
from google import genai

from retrieve_utils import retrieve_context


# ==========================================
# Load API Key
# ==========================================

load_dotenv()

api_key = os.getenv("AQ.Ab8RN6KlzvBXjjfRPXGn9pRewKhq3Fh26wvwg4SwUXm_VX1gag")

client = genai.Client(
    api_key=api_key
)


# ==========================================
# Streamlit Configuration
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
# User Input
# ==========================================

query = st.text_input(
    "Enter your product question:"
)


# ==========================================
# Run RAG Pipeline
# ==========================================

if st.button("Get Answer"):

    if query:

        with st.spinner("Searching and generating answer..."):


            # ------------------------------
            # Retrieval
            # ------------------------------

            context, retrieved_chunks = retrieve_context(query)



            # ------------------------------
            # Prompt
            # ------------------------------

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


            # ------------------------------
            # Gemini Generation
            # ------------------------------

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )


            answer = response.text



        # ==================================
        # Display Answer
        # ==================================

        st.subheader("Answer")

        st.success(answer)



        # ==================================
        # Show Retrieved Context
        # ==================================

        with st.expander(
            "View Retrieved Documents"
        ):

            for i, item in enumerate(
                retrieved_chunks,
                start=1
            ):

                st.write(
                    f"### Document {i}"
                )

                st.write(
                    item["document"]
                )

