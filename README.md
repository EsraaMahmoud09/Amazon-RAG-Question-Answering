# Amazon-RAG-Question-Answering
# Amazon Product Question Answering using RAG

> Retrieval-Augmented Generation (RAG) system for answering Amazon product questions using Hybrid Search, Cross-Encoder Reranking, ChromaDB, and Google Gemini.

---

## Project Overview

This project implements an end-to-end Retrieval-Augmented Generation (RAG) pipeline for Amazon Product Question Answering.

The system retrieves the most relevant product question-answer pairs using a hybrid retrieval approach that combines semantic search and lexical search. Retrieved results are then reranked using a Cross-Encoder model before being passed to Google Gemini for answer generation.

The application is deployed with **Streamlit**, providing an interactive interface where users can ask product-related questions and receive context-aware answers.

---

## Dataset

This project uses the **Amazon Question Answer Dataset** available on Kaggle:

**Dataset:**
https://www.kaggle.com/datasets/praneshmukhopadhyay/amazon-questionanswer-dataset

Only the following files from the dataset were used:

* `multi_questions.csv`
* `multi_answers.csv`

The dataset contains Amazon customer questions and corresponding answers across multiple product categories.

---

## Project Pipeline

1. Data preprocessing and cleaning
2. Semantic text preparation
3. Text chunking
4. Embedding generation using Sentence Transformers
5. ChromaDB vector database creation
6. BM25 lexical retrieval
7. Hybrid Retrieval (Semantic + BM25)
8. Cross-Encoder reranking
9. Context construction
10. Answer generation using Google Gemini
11. Streamlit web application deployment

---

## Technologies

* Python
* Pandas
* Sentence Transformers
* ChromaDB
* BM25
* Cross-Encoder
* Google Gemini API
* Streamlit

---

## Streamlit Application

### Application Preview

> *(Add your Streamlit screenshot here)*

<p align="center">
<img src="images/streamlit_app.png" width="900">
</p>

---

## Repository Structure

```text
Amazon-RAG-Question-Answering/
│
├── notebooks/
├── streamlit_app.py
├── retrieve_utils.py
├── requirements.txt
├── README.md
├── notebooks/
│   ├── 01_Data_Loading.ipynb
│   ├── 02_Preprocessing.ipynb
│   ├── 03_Chunking.ipynb
│   ├── 04_Embeddings.ipynb
│   ├── 05_ChromaDB.ipynb
│   ├── 06_Retrieval.ipynb
│   ├── 07_Reranking.ipynb
│   ├── 08_Context_Building.ipynb
│   ├── 09_RAG.ipynb
│   └── 10_Evaluation.ipynb
├── data/
│   ├── multi_questions.csv
│   ├── multi_answers.csv
│   ├── cleaned_dataset.csv
│   ├── chunks.csv
│   └── embeddings.npy
│
└── chroma_db/

## Author

**Esraa Mahmoud**

📧 Email: esraashawky09@gmail.com

💼 LinkedIn: www.linkedin.com/in/esraa-mahmoud22



