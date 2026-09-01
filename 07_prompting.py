{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 21,
   "id": "5e95dc50-b58c-4440-a526-c63a6ffc43e1",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The autoreload extension is already loaded. To reload it, use:\n",
      "  %reload_ext autoreload\n"
     ]
    }
   ],
   "source": [
    "%load_ext autoreload\n",
    "%autoreload 2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "02fba870-af90-4d51-9c60-e14186e85aa3",
   "metadata": {},
   "outputs": [
    {
     "ename": "KeyError",
     "evalue": "\"['QuestionText'] not in index\"",
     "output_type": "error",
     "traceback": [
      "\u001b[31m---------------------------------------------------------------------------\u001b[39m",
      "\u001b[31mKeyError\u001b[39m                                  Traceback (most recent call last)",
      "\u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[22]\u001b[39m\u001b[32m, line 3\u001b[39m\n\u001b[32m      1\u001b[39m \u001b[38;5;66;03m# خلية تجربة واختبار للـ Hybrid Search\u001b[39;00m\n\u001b[32m      2\u001b[39m results = retrieve_utils.hybrid_search(\u001b[33m\"will they fit 2013 f350 dually\"\u001b[39m, semantic_k=\u001b[32m10\u001b[39m, lexical_k=\u001b[32m10\u001b[39m)\n\u001b[32m----> \u001b[39m\u001b[32m3\u001b[39m print(\u001b[33m\"Lexical:\"\u001b[39m, results[\u001b[33m\"lexical\"\u001b[39m][[\u001b[33m\"QuestionText\"\u001b[39m, \u001b[33m\"bm25_score\"\u001b[39m]])\n",
      "\u001b[36mFile \u001b[39m\u001b[32m~\\.conda\\envs\\rag\\Lib\\site-packages\\pandas\\core\\frame.py:4384\u001b[39m, in \u001b[36mDataFrame.__getitem__\u001b[39m\u001b[34m(self, key)\u001b[39m\n\u001b[32m   4380\u001b[39m                 indexer = [indexer]\n\u001b[32m   4381\u001b[39m         \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[32m   4382\u001b[39m             \u001b[38;5;28;01mif\u001b[39;00m is_iterator(key):\n\u001b[32m   4383\u001b[39m                 key = list(key)\n\u001b[32m-> \u001b[39m\u001b[32m4384\u001b[39m             indexer = self.columns._get_indexer_strict(key, \u001b[33m\"columns\"\u001b[39m)[\u001b[32m1\u001b[39m]\n\u001b[32m   4385\u001b[39m \n\u001b[32m   4386\u001b[39m         \u001b[38;5;66;03m# take() does not accept boolean indexers\u001b[39;00m\n\u001b[32m   4387\u001b[39m         \u001b[38;5;28;01mif\u001b[39;00m getattr(indexer, \u001b[33m\"dtype\"\u001b[39m, \u001b[38;5;28;01mNone\u001b[39;00m) == bool:\n",
      "\u001b[36mFile \u001b[39m\u001b[32m~\\.conda\\envs\\rag\\Lib\\site-packages\\pandas\\core\\indexes\\base.py:6302\u001b[39m, in \u001b[36mIndex._get_indexer_strict\u001b[39m\u001b[34m(self, key, axis_name)\u001b[39m\n\u001b[32m   6299\u001b[39m \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[32m   6300\u001b[39m     keyarr, indexer, new_indexer = \u001b[38;5;28mself\u001b[39m._reindex_non_unique(keyarr)\n\u001b[32m-> \u001b[39m\u001b[32m6302\u001b[39m \u001b[30;43mself\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43m_raise_if_missing\u001b[39;49m\u001b[30;43m(\u001b[39;49m\u001b[30;43mkeyarr\u001b[39;49m\u001b[30;43m,\u001b[39;49m\u001b[30;43m \u001b[39;49m\u001b[30;43mindexer\u001b[39;49m\u001b[30;43m,\u001b[39;49m\u001b[30;43m \u001b[39;49m\u001b[30;43maxis_name\u001b[39;49m\u001b[30;43m)\u001b[39;49m\n\u001b[32m   6304\u001b[39m keyarr = \u001b[38;5;28mself\u001b[39m.take(indexer)\n\u001b[32m   6305\u001b[39m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;28misinstance\u001b[39m(key, Index):\n\u001b[32m   6306\u001b[39m     \u001b[38;5;66;03m# GH 42790 - Preserve name from an Index\u001b[39;00m\n",
      "\u001b[36mFile \u001b[39m\u001b[32m~\\.conda\\envs\\rag\\Lib\\site-packages\\pandas\\core\\indexes\\base.py:6355\u001b[39m, in \u001b[36mIndex._raise_if_missing\u001b[39m\u001b[34m(self, key, indexer, axis_name)\u001b[39m\n\u001b[32m   6352\u001b[39m     \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mKeyError\u001b[39;00m(\u001b[33mf\u001b[39m\u001b[33m\"\u001b[39m\u001b[33mNone of [\u001b[39m\u001b[38;5;132;01m{\u001b[39;00mkey\u001b[38;5;132;01m}\u001b[39;00m\u001b[33m] are in the [\u001b[39m\u001b[38;5;132;01m{\u001b[39;00maxis_name\u001b[38;5;132;01m}\u001b[39;00m\u001b[33m]\u001b[39m\u001b[33m\"\u001b[39m)\n\u001b[32m   6354\u001b[39m not_found = \u001b[38;5;28mlist\u001b[39m(ensure_index(key)[missing_mask.nonzero()[\u001b[32m0\u001b[39m]].unique())\n\u001b[32m-> \u001b[39m\u001b[32m6355\u001b[39m \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mKeyError\u001b[39;00m(\u001b[33mf\u001b[39m\u001b[33m\"\u001b[39m\u001b[38;5;132;01m{\u001b[39;00mnot_found\u001b[38;5;132;01m}\u001b[39;00m\u001b[33m not in index\u001b[39m\u001b[33m\"\u001b[39m)\n",
      "\u001b[31mKeyError\u001b[39m: \"['QuestionText'] not in index\""
     ]
    }
   ],
   "source": [
    "# خلية تجربة واختبار للـ Hybrid Search\n",
    "results = retrieve_utils.hybrid_search(\"will they fit 2013 f350 dually\", semantic_k=10, lexical_k=10)\n",
    "print(\"Lexical:\", results[\"lexical\"][[\"QuestionText\", \"bm25_score\"]])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "559eda54-f084-49b7-8650-a392c68b655a",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>chunk_id</th>\n",
       "      <th>chunk_text</th>\n",
       "      <th>bm25_score</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>5713</th>\n",
       "      <td>row_5450_chunk_0</td>\n",
       "      <td>need plug adapter make fit 2005 f350 cant real...</td>\n",
       "      <td>14.493105</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2297</th>\n",
       "      <td>row_2182_chunk_0</td>\n",
       "      <td>flairs use double sided tape screws flares wer...</td>\n",
       "      <td>13.259904</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>15347</th>\n",
       "      <td>row_14688_chunk_0</td>\n",
       "      <td>really fit perfectly 2013 4runner yes purchase...</td>\n",
       "      <td>12.056008</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5241</th>\n",
       "      <td>row_4996_chunk_0</td>\n",
       "      <td>rapid jack work regular car suv multiaxle trai...</td>\n",
       "      <td>11.648551</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6273</th>\n",
       "      <td>row_5988_chunk_0</td>\n",
       "      <td>would work 2013 mdx helloit fit perfectly 2013...</td>\n",
       "      <td>11.201513</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>17999</th>\n",
       "      <td>row_17219_chunk_0</td>\n",
       "      <td>fit 2013 model passenger</td>\n",
       "      <td>11.090616</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5482</th>\n",
       "      <td>row_5227_chunk_0</td>\n",
       "      <td>would fit rzr 800 2013 fits 2011 rzr800 think ...</td>\n",
       "      <td>11.048365</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>13289</th>\n",
       "      <td>row_12737_chunk_0</td>\n",
       "      <td>fit commander 1000x 2013 2 spacers</td>\n",
       "      <td>10.604259</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>14785</th>\n",
       "      <td>row_14152_chunk_0</td>\n",
       "      <td>fit 2013 jeep wrangler unlimited yes</td>\n",
       "      <td>10.604259</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3920</th>\n",
       "      <td>row_3723_chunk_0</td>\n",
       "      <td>2013 spyder st limited fit yes cover really bi...</td>\n",
       "      <td>10.214202</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                chunk_id                                         chunk_text  \\\n",
       "5713    row_5450_chunk_0  need plug adapter make fit 2005 f350 cant real...   \n",
       "2297    row_2182_chunk_0  flairs use double sided tape screws flares wer...   \n",
       "15347  row_14688_chunk_0  really fit perfectly 2013 4runner yes purchase...   \n",
       "5241    row_4996_chunk_0  rapid jack work regular car suv multiaxle trai...   \n",
       "6273    row_5988_chunk_0  would work 2013 mdx helloit fit perfectly 2013...   \n",
       "17999  row_17219_chunk_0                           fit 2013 model passenger   \n",
       "5482    row_5227_chunk_0  would fit rzr 800 2013 fits 2011 rzr800 think ...   \n",
       "13289  row_12737_chunk_0                 fit commander 1000x 2013 2 spacers   \n",
       "14785  row_14152_chunk_0               fit 2013 jeep wrangler unlimited yes   \n",
       "3920    row_3723_chunk_0  2013 spyder st limited fit yes cover really bi...   \n",
       "\n",
       "       bm25_score  \n",
       "5713    14.493105  \n",
       "2297    13.259904  \n",
       "15347   12.056008  \n",
       "5241    11.648551  \n",
       "6273    11.201513  \n",
       "17999   11.090616  \n",
       "5482    11.048365  \n",
       "13289   10.604259  \n",
       "14785   10.604259  \n",
       "3920    10.214202  "
      ]
     },
     "execution_count": 23,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "results[\"lexical\"][[\"chunk_id\", \"chunk_text\", \"bm25_score\"]]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "id": "15bfec5d-c772-4ff7-9c1d-849e13304180",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Admin\\Desktop\\Digilians\\Second Term\\AI Applied and Tools\\RAG\\New folder\\retrieve_utils.py\n",
      "['BM25Okapi', 'CrossEncoder', 'SentenceTransformer', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'bm25', 'build_context', 'chromadb', 'client', 'collection', 'embedding_model', 'hybrid_search', 'lexical_dataset', 'lexical_search', 'np', 'pd', 'remove_duplicates', 'rerank_results', 'reranker', 'retrieve_context', 'semantic_search']\n"
     ]
    }
   ],
   "source": [
    "import retrieve_utils\n",
    "\n",
    "print(retrieve_utils.__file__)\n",
    "\n",
    "print(dir(retrieve_utils))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "84c0aac7-a05b-4f93-b49a-0dbf48c34928",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "e93ad7aa2cf7481b96e2e9bdfdab54b4",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Loading weights:   0%|          | 0/103 [00:00<?, ?it/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "c2b411dc3f654c2ca386187847ca7288",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Loading weights:   0%|          | 0/105 [00:00<?, ?it/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import importlib\n",
    "import retrieve_utils\n",
    "\n",
    "importlib.reload(retrieve_utils)\n",
    "\n",
    "from retrieve_utils import retrieve_context"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "id": "d9d9b9c4-1462-4248-a5a9-9277bba02126",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "def semantic_search(query, top_k=5):\n",
      "\n",
      "    query_embedding = embedding_model.encode(\n",
      "        query,\n",
      "        normalize_embeddings=True\n",
      "    ).tolist()\n",
      "\n",
      "    results = collection.query(\n",
      "        query_embeddings=[query_embedding],\n",
      "        n_results=top_k,\n",
      "        include=[\n",
      "            \"documents\",\n",
      "            \"metadatas\",\n",
      "            \"distances\"\n",
      "        ],\n",
      "    )\n",
      "\n",
      "    return results\n",
      "\n"
     ]
    }
   ],
   "source": [
    "import inspect\n",
    "import retrieve_utils\n",
    "\n",
    "print(inspect.getsource(retrieve_utils.semantic_search))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "id": "323e2bb7-7cfd-4df1-a399-b4a9c8d43c43",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "def lexical_search(query, top_k=5):  # تم إضافة top_k كـ argument لتفادي TypeError\n",
      "\n",
      "    query_tokens = query.lower().split()\n",
      "    scores = bm25.get_scores(query_tokens)\n",
      "    top_indices = scores.argsort()[-top_k:][::-1]\n",
      "    results = lexical_dataset.iloc[top_indices].copy()\n",
      "    results[\"bm25_score\"] = scores[top_indices]\n",
      "\n",
      "    return results\n",
      "\n"
     ]
    }
   ],
   "source": [
    "import inspect\n",
    "import retrieve_utils\n",
    "\n",
    "print(inspect.getsource(retrieve_utils.lexical_search))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "id": "9ca5cfe7-3ac7-4612-aabc-3811d5221d37",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "d5c5e82fbd0d4f1e8ffa8c72851ae711",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Loading weights:   0%|          | 0/103 [00:00<?, ?it/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "c064ce6d623640e9814e2ad892286524",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Loading weights:   0%|          | 0/105 [00:00<?, ?it/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "def lexical_search(query, top_k=5):  # تم إضافة top_k كـ argument لتفادي TypeError\n",
      "\n",
      "    query_tokens = query.lower().split()\n",
      "    scores = bm25.get_scores(query_tokens)\n",
      "    top_indices = scores.argsort()[-top_k:][::-1]\n",
      "    results = lexical_dataset.iloc[top_indices].copy()\n",
      "    results[\"bm25_score\"] = scores[top_indices]\n",
      "\n",
      "    return results\n",
      "\n"
     ]
    }
   ],
   "source": [
    "import importlib\n",
    "import retrieve_utils\n",
    "\n",
    "importlib.reload(retrieve_utils)\n",
    "\n",
    "print(inspect.getsource(retrieve_utils.lexical_search))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "id": "95378ee2-74ed-4815-aede-1d831daed5cb",
   "metadata": {},
   "outputs": [],
   "source": [
    "# =============================================================================\n",
    "# Import Required Libraries\n",
    "# =============================================================================\n",
    "# Data manipulation and loading datasets\n",
    "import pandas as pd\n",
    "\n",
    "# Google AI Studio client for interacting with Large Language Models (LLMs)\n",
    "# Google Gemini API\n",
    "from google import genai"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "id": "c1eb0907-5806-432e-9fcc-b106c359b0ec",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Retrieve module loaded successfully.\n"
     ]
    }
   ],
   "source": [
    "# ==========================================================\n",
    "# Import Retrieval Pipeline\n",
    "# ==========================================================\n",
    "from retrieve_utils import retrieve_context\n",
    "\n",
    "print(\"Retrieve module loaded successfully.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 64,
   "id": "ef850895-7c34-4a57-84e8-18e9b1cb7b3c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Ask your question:  will the westbend 6qt versatility oblong slowcooker and base fit in this bag?\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# User Question\n",
    "# =============================================================================\n",
    "query = input(\"Ask your question: \")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 65,
   "id": "c01acc90-4d9b-43b0-a98a-ccd72f16049f",
   "metadata": {},
   "outputs": [],
   "source": [
    "# =============================================================================\n",
    "# Retrieve Relevant Context\n",
    "# Generate the final context using the complete RAG retrieval pipeline\n",
    "# (Hybrid Search → Reranking → Duplicate Removal → Context Building)\n",
    "# =============================================================================\n",
    "context, retrieved_chunks = retrieve_context(query)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 66,
   "id": "95e89f86-e031-42d2-932c-06f1311f95bf",
   "metadata": {},
   "outputs": [],
   "source": [
    "# =============================================================================\n",
    "# Prompt Template\n",
    "# =============================================================================\n",
    "system_instruction = \"\"\"\n",
    "You are a strict Amazon Product Question Answering Assistant.\n",
    "\n",
    "CRITICAL INSTRUCTIONS:\n",
    "1. Answer ONLY using the provided Context.\n",
    "2. ABSENCE IS NOT NEGATION: If the Context mentions a product review but DOES NOT explicitly state whether a feature exists (e.g., liner, zipper, size), you MUST NOT say \"No\" or infer that it lacks the feature.\n",
    "3. If the context does not explicitly contain the answer, your output MUST BE EXACTLY:\n",
    "   \"I don't have enough information from the available product reviews to answer this question.\"\n",
    "4. Do NOT add intros like \"Based on the available information\" or explain your reasoning. \"\"\"\n",
    "\n",
    "prompt = f\"\"\"\n",
    "You are an expert Amazon Product Question Answering Assistant using a ReAct-style approach.\n",
    "\n",
    "Your goal is to answer customer questions accurately using the retrieved product context.\n",
    "\n",
    "Follow this process internally:\n",
    "\n",
    "1. Analyze:\n",
    "- Identify the required information (fit, size, compatibility, capacity, usage, etc.).\n",
    "\n",
    "2. Retrieve Evidence:\n",
    "- Examine the provided context.\n",
    "- Select only information relevant to the question.\n",
    "- Compare multiple reviews if available.\n",
    "\n",
    "3. Decide:\n",
    "- Determine the best answer based on the available evidence.\n",
    "- If information is conflicting, explain the uncertainty.\n",
    "- If information is missing, do not guess.\n",
    "\n",
    "4. Respond:\n",
    "- Provide a clear and concise customer-friendly answer.\n",
    "- Rewrite the information naturally.\n",
    "- Do not copy the context word-for-word.\n",
    "- Do not mention this reasoning process.\n",
    "\n",
    "Rules:\n",
    "- Use ONLY the provided context.\n",
    "- Never invent product specifications.\n",
    "- If the context does not provide enough evidence, answer:\n",
    "  \"I don't have enough information from the available product reviews to answer this question.\"\n",
    "\n",
    "Retrieved Context:\n",
    "{context}\n",
    "\n",
    "Customer Question:\n",
    "{query}\n",
    "\n",
    "Final Answer:\n",
    "\"\"\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 67,
   "id": "a3907ca2-1753-4c7a-ab42-f097bb717dbe",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Context 1\n",
      "Question: will the westbend 6qt versatility oblong slowcooker and base fit in this bag? Answer: i have not tested it long term-just to transport an already hot pot to a dinner and serve directly. i had another insulated bag which this one is replacing due to some unfortunate damage (unrelated to the crockpot) that kept food nice and hot for at least an hour. this one seems a bit thinner, so i am thinking at least 30 minutes? it does fit nice and snugly to the appliance so i would expect it to retain heat reasonably well.\n",
      "\n",
      "Context 2\n",
      "westbend 6qt versatility oblong slowcooker base fit bag tested long termjust transport already hot pot dinner serve directly another insulated bag one replacing due unfortunate damage unrelated crockpot kept food nice hot least hour one seems bit thinner thinking least 30 minutes fit nice snugly appliance would expect retain heat reasonably well\n",
      "\n",
      "Context 3\n",
      "Question: will this fit a professional 6 qt. mixer? Answer: no, it will not. the cover is a snug fit for a standard 4qt. mixer.\n",
      "\n",
      "Context 4\n",
      "Question: i have a fender cd-100ce dreadnought cutaway acoustic-electric guitar, left handed - natural. will it fit in this bag? Answer: i don't know for certain, however i did a google search of your guitar and it looks similar to the acoustic guitar i'm using this fender bag for. it's pretty roomy so i'm fairly certain your guitar will fit. i hope that helps. happy shopping.\n",
      "\n",
      "Context 5\n",
      "Question: silly question ..... how are the pedals affixed to the bag? Answer: i was able to fit a line 6 pod hd 500 in this bag. check the line 6 website to see if those dimensions are at least greater than or equal to your pedal board measurements.\n",
      "\n",
      "\n"
     ]
    }
   ],
   "source": [
    "print(context)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 68,
   "id": "b82e77f4-9fcb-486b-accd-528c50cf3397",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Yes, the Westbend 6qt versatility oblong slowcooker and base will fit in this bag. It is described as fitting \"nice and snugly\" to the appliance.\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# Generate Response\n",
    "# =============================================================================\n",
    "client = genai.Client(api_key=\"AQ.Ab8RN6KlzvBXjjfRPXGn9pRewKhq3Fh26wvwg4SwUXm_VX1gag\")\n",
    "\n",
    "response = client.models.generate_content(\n",
    "    model=\"gemini-2.5-flash\",\n",
    "    contents=prompt,\n",
    "    config={\"temperature\": 0.0})\n",
    "\n",
    "answer = response.text\n",
    "\n",
    "print(answer)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python (RAG)",
   "language": "python",
   "name": "rag"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.15"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
