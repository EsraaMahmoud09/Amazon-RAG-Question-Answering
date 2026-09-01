{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "b43bb930-571c-4532-a8f7-b7e4d40d294b",
   "metadata": {},
   "outputs": [],
   "source": [
    "# =============================================================================\n",
    "# Data Processing\n",
    "# =============================================================================\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "\n",
    "import re\n",
    "\n",
    "# =============================================================================\n",
    "# Embedding Models\n",
    "# =============================================================================\n",
    "from sentence_transformers import SentenceTransformer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "dd8171e3-a15d-4e47-8067-a8c5a186e91b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(22558, 8)\n"
     ]
    },
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
       "      <th>QuestionID</th>\n",
       "      <th>Category</th>\n",
       "      <th>QuestionType</th>\n",
       "      <th>QuestionTime</th>\n",
       "      <th>chunk_index</th>\n",
       "      <th>chunk_text</th>\n",
       "      <th>search_text</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>C15Q2112_row_0_c_0</td>\n",
       "      <td>C15Q2112</td>\n",
       "      <td>Tools and Home Improvement</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2013-04-20</td>\n",
       "      <td>0</td>\n",
       "      <td>Question: - what are the dimensions of this it...</td>\n",
       "      <td>Category: Tools and Home Improvement Question ...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>C9Q4595_row_1_c_0</td>\n",
       "      <td>C9Q4595</td>\n",
       "      <td>Home and Kitchen</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-02-06</td>\n",
       "      <td>0</td>\n",
       "      <td>Question: how much booze can it hold? Answer: ...</td>\n",
       "      <td>Category: Home and Kitchen Question Type: open...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>C4Q7999_row_2_c_0</td>\n",
       "      <td>C4Q7999</td>\n",
       "      <td>Cell Phones and Accessories</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-08-09</td>\n",
       "      <td>0</td>\n",
       "      <td>Question: will this case fit nokia lumia 520 A...</td>\n",
       "      <td>Category: Cell Phones and Accessories Question...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>C8Q8916_row_3_c_0</td>\n",
       "      <td>C8Q8916</td>\n",
       "      <td>Health and Personal Care</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-04-25</td>\n",
       "      <td>0</td>\n",
       "      <td>Question: when folded in the sitting position,...</td>\n",
       "      <td>Category: Health and Personal Care Question Ty...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>C14Q905_row_4_c_0</td>\n",
       "      <td>C14Q905</td>\n",
       "      <td>Sports and Outdoors</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2015-04-15</td>\n",
       "      <td>0</td>\n",
       "      <td>Question: how long should i leave this on to g...</td>\n",
       "      <td>Category: Sports and Outdoors Question Type: o...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "             chunk_id QuestionID                     Category QuestionType  \\\n",
       "0  C15Q2112_row_0_c_0   C15Q2112   Tools and Home Improvement   open-ended   \n",
       "1   C9Q4595_row_1_c_0    C9Q4595             Home and Kitchen   open-ended   \n",
       "2   C4Q7999_row_2_c_0    C4Q7999  Cell Phones and Accessories   open-ended   \n",
       "3   C8Q8916_row_3_c_0    C8Q8916     Health and Personal Care   open-ended   \n",
       "4   C14Q905_row_4_c_0    C14Q905          Sports and Outdoors   open-ended   \n",
       "\n",
       "  QuestionTime  chunk_index  \\\n",
       "0   2013-04-20            0   \n",
       "1   2014-02-06            0   \n",
       "2   2014-08-09            0   \n",
       "3   2014-04-25            0   \n",
       "4   2015-04-15            0   \n",
       "\n",
       "                                          chunk_text  \\\n",
       "0  Question: - what are the dimensions of this it...   \n",
       "1  Question: how much booze can it hold? Answer: ...   \n",
       "2  Question: will this case fit nokia lumia 520 A...   \n",
       "3  Question: when folded in the sitting position,...   \n",
       "4  Question: how long should i leave this on to g...   \n",
       "\n",
       "                                         search_text  \n",
       "0  Category: Tools and Home Improvement Question ...  \n",
       "1  Category: Home and Kitchen Question Type: open...  \n",
       "2  Category: Cell Phones and Accessories Question...  \n",
       "3  Category: Health and Personal Care Question Ty...  \n",
       "4  Category: Sports and Outdoors Question Type: o...  "
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# Load semantic_dataset documents\n",
    "# =============================================================================\n",
    "semantic_dataset = pd.read_csv(\"semantic_chunks.csv\")\n",
    "print(semantic_dataset.shape)\n",
    "semantic_dataset.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "ef57cdbe-710a-42f5-bf0b-b9ae13184b0b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['chunk_id', 'QuestionID', 'Category', 'QuestionType', 'QuestionTime',\n",
       "       'chunk_index', 'chunk_text', 'search_text'],\n",
       "      dtype='str')"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "semantic_dataset.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "bc66b4fa-3f65-4966-98c8-92115af69409",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(20916, 8)\n"
     ]
    },
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
       "      <th>QuestionID</th>\n",
       "      <th>Category</th>\n",
       "      <th>QuestionType</th>\n",
       "      <th>QuestionTime</th>\n",
       "      <th>chunk_index</th>\n",
       "      <th>chunk_text</th>\n",
       "      <th>search_text</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>row_0_chunk_0</td>\n",
       "      <td>C15Q2112</td>\n",
       "      <td>Tools and Home Improvement</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2013-04-20</td>\n",
       "      <td>0</td>\n",
       "      <td>dimensions item</td>\n",
       "      <td>Tools and Home Improvement open-ended dimensio...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>row_1_chunk_0</td>\n",
       "      <td>C9Q4595</td>\n",
       "      <td>Home and Kitchen</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-02-06</td>\n",
       "      <td>0</td>\n",
       "      <td>much booze hold poured booze measuring cup sun...</td>\n",
       "      <td>Home and Kitchen open-ended much booze hold po...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>row_2_chunk_0</td>\n",
       "      <td>C4Q7999</td>\n",
       "      <td>Cell Phones and Accessories</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-08-09</td>\n",
       "      <td>0</td>\n",
       "      <td>case fit nokia lumia 520 yes fits great great ...</td>\n",
       "      <td>Cell Phones and Accessories open-ended case fi...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>row_3_chunk_0</td>\n",
       "      <td>C8Q8916</td>\n",
       "      <td>Health and Personal Care</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-04-25</td>\n",
       "      <td>0</td>\n",
       "      <td>folded sitting position high ground seat 30 in...</td>\n",
       "      <td>Health and Personal Care open-ended folded sit...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>row_4_chunk_0</td>\n",
       "      <td>C14Q905</td>\n",
       "      <td>Sports and Outdoors</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2015-04-15</td>\n",
       "      <td>0</td>\n",
       "      <td>long leave get max sweat benefit keep thinking...</td>\n",
       "      <td>Sports and Outdoors open-ended long leave get ...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "        chunk_id QuestionID                     Category QuestionType  \\\n",
       "0  row_0_chunk_0   C15Q2112   Tools and Home Improvement   open-ended   \n",
       "1  row_1_chunk_0    C9Q4595             Home and Kitchen   open-ended   \n",
       "2  row_2_chunk_0    C4Q7999  Cell Phones and Accessories   open-ended   \n",
       "3  row_3_chunk_0    C8Q8916     Health and Personal Care   open-ended   \n",
       "4  row_4_chunk_0    C14Q905          Sports and Outdoors   open-ended   \n",
       "\n",
       "  QuestionTime  chunk_index  \\\n",
       "0   2013-04-20            0   \n",
       "1   2014-02-06            0   \n",
       "2   2014-08-09            0   \n",
       "3   2014-04-25            0   \n",
       "4   2015-04-15            0   \n",
       "\n",
       "                                          chunk_text  \\\n",
       "0                                    dimensions item   \n",
       "1  much booze hold poured booze measuring cup sun...   \n",
       "2  case fit nokia lumia 520 yes fits great great ...   \n",
       "3  folded sitting position high ground seat 30 in...   \n",
       "4  long leave get max sweat benefit keep thinking...   \n",
       "\n",
       "                                         search_text  \n",
       "0  Tools and Home Improvement open-ended dimensio...  \n",
       "1  Home and Kitchen open-ended much booze hold po...  \n",
       "2  Cell Phones and Accessories open-ended case fi...  \n",
       "3  Health and Personal Care open-ended folded sit...  \n",
       "4  Sports and Outdoors open-ended long leave get ...  "
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# Load lexical_dataset documents\n",
    "# =============================================================================\n",
    "lexical_dataset = pd.read_csv(\"lexical_chunks.csv\")\n",
    "print(lexical_dataset.shape)\n",
    "lexical_dataset.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "86e037b1-d930-4b04-9033-0962a10926ef",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['chunk_id', 'QuestionID', 'Category', 'QuestionType', 'QuestionTime',\n",
       "       'chunk_index', 'chunk_text', 'search_text'],\n",
       "      dtype='str')"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "lexical_dataset.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "ac1a82fd-b80d-4cd4-b915-c4658701102c",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.\n"
     ]
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "dac7cf37ae7a4e08bc0a1f0c8c67d11b",
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
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Embedding model loaded successfully.\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# Load SentenceTransformer Model\n",
    "# =============================================================================\n",
    "embedding_model = SentenceTransformer(\"sentence-transformers/all-MiniLM-L6-v2\")\n",
    "print(\"Embedding model loaded successfully.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "aa6e2706-3514-4d97-bccf-f8bcaf0c218d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Total Chunks: 22558\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# Prepare Semantic Documents\n",
    "# =============================================================================\n",
    "documents = semantic_dataset[\"search_text\"].tolist()\n",
    "print(\"Total Chunks:\", len(documents))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "080e788a-d11c-4947-8f6c-fecf7f701b65",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "f82d6a784b5f4a8fb7828cda2721ecd5",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "Batches:   0%|          | 0/705 [00:00<?, ?it/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(22558, 384)\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# Generate Sentence Embeddings\n",
    "# =============================================================================\n",
    "embeddings = embedding_model.encode(\n",
    "    documents,\n",
    "    batch_size=32,\n",
    "    show_progress_bar=True,\n",
    "    convert_to_numpy=True,\n",
    "    normalize_embeddings=True)\n",
    "\n",
    "print(embeddings.shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "95919922-b912-47fa-a456-6b30c1c54565",
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
       "      <th>QuestionID</th>\n",
       "      <th>Category</th>\n",
       "      <th>QuestionType</th>\n",
       "      <th>QuestionTime</th>\n",
       "      <th>chunk_index</th>\n",
       "      <th>chunk_text</th>\n",
       "      <th>search_text</th>\n",
       "      <th>embedding</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>C15Q2112_row_0_c_0</td>\n",
       "      <td>C15Q2112</td>\n",
       "      <td>Tools and Home Improvement</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2013-04-20</td>\n",
       "      <td>0</td>\n",
       "      <td>Question: - what are the dimensions of this it...</td>\n",
       "      <td>Category: Tools and Home Improvement Question ...</td>\n",
       "      <td>[0.005750724114477634, 0.0893775224685669, -0....</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>C9Q4595_row_1_c_0</td>\n",
       "      <td>C9Q4595</td>\n",
       "      <td>Home and Kitchen</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-02-06</td>\n",
       "      <td>0</td>\n",
       "      <td>Question: how much booze can it hold? Answer: ...</td>\n",
       "      <td>Category: Home and Kitchen Question Type: open...</td>\n",
       "      <td>[0.10887277871370316, 0.08158908039331436, -0....</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>C4Q7999_row_2_c_0</td>\n",
       "      <td>C4Q7999</td>\n",
       "      <td>Cell Phones and Accessories</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-08-09</td>\n",
       "      <td>0</td>\n",
       "      <td>Question: will this case fit nokia lumia 520 A...</td>\n",
       "      <td>Category: Cell Phones and Accessories Question...</td>\n",
       "      <td>[-0.11016276478767395, 0.046286050230264664, 0...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>C8Q8916_row_3_c_0</td>\n",
       "      <td>C8Q8916</td>\n",
       "      <td>Health and Personal Care</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-04-25</td>\n",
       "      <td>0</td>\n",
       "      <td>Question: when folded in the sitting position,...</td>\n",
       "      <td>Category: Health and Personal Care Question Ty...</td>\n",
       "      <td>[0.028559448197484016, 0.017597395926713943, 0...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>C14Q905_row_4_c_0</td>\n",
       "      <td>C14Q905</td>\n",
       "      <td>Sports and Outdoors</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2015-04-15</td>\n",
       "      <td>0</td>\n",
       "      <td>Question: how long should i leave this on to g...</td>\n",
       "      <td>Category: Sports and Outdoors Question Type: o...</td>\n",
       "      <td>[-0.0072077070362865925, 0.05245823785662651, ...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "             chunk_id QuestionID                     Category QuestionType  \\\n",
       "0  C15Q2112_row_0_c_0   C15Q2112   Tools and Home Improvement   open-ended   \n",
       "1   C9Q4595_row_1_c_0    C9Q4595             Home and Kitchen   open-ended   \n",
       "2   C4Q7999_row_2_c_0    C4Q7999  Cell Phones and Accessories   open-ended   \n",
       "3   C8Q8916_row_3_c_0    C8Q8916     Health and Personal Care   open-ended   \n",
       "4   C14Q905_row_4_c_0    C14Q905          Sports and Outdoors   open-ended   \n",
       "\n",
       "  QuestionTime  chunk_index  \\\n",
       "0   2013-04-20            0   \n",
       "1   2014-02-06            0   \n",
       "2   2014-08-09            0   \n",
       "3   2014-04-25            0   \n",
       "4   2015-04-15            0   \n",
       "\n",
       "                                          chunk_text  \\\n",
       "0  Question: - what are the dimensions of this it...   \n",
       "1  Question: how much booze can it hold? Answer: ...   \n",
       "2  Question: will this case fit nokia lumia 520 A...   \n",
       "3  Question: when folded in the sitting position,...   \n",
       "4  Question: how long should i leave this on to g...   \n",
       "\n",
       "                                         search_text  \\\n",
       "0  Category: Tools and Home Improvement Question ...   \n",
       "1  Category: Home and Kitchen Question Type: open...   \n",
       "2  Category: Cell Phones and Accessories Question...   \n",
       "3  Category: Health and Personal Care Question Ty...   \n",
       "4  Category: Sports and Outdoors Question Type: o...   \n",
       "\n",
       "                                           embedding  \n",
       "0  [0.005750724114477634, 0.0893775224685669, -0....  \n",
       "1  [0.10887277871370316, 0.08158908039331436, -0....  \n",
       "2  [-0.11016276478767395, 0.046286050230264664, 0...  \n",
       "3  [0.028559448197484016, 0.017597395926713943, 0...  \n",
       "4  [-0.0072077070362865925, 0.05245823785662651, ...  "
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# Store Embeddings\n",
    "# =============================================================================\n",
    "semantic_dataset[\"embedding\"] = embeddings.tolist()\n",
    "semantic_dataset.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "b31bc512-55ac-4ae7-a8fa-c02c9a3af8bf",
   "metadata": {},
   "outputs": [],
   "source": [
    "# =============================================================================\n",
    "# BM25 Tokenizer\n",
    "# =============================================================================\n",
    "def tokenize_text(text):\n",
    "\n",
    "    \"\"\"\n",
    "    Tokenize text for BM25 indexing.\n",
    "    \"\"\"\n",
    "\n",
    "    return re.findall(\n",
    "        r\"\\b[a-zA-Z0-9]+\\b\",\n",
    "        str(text).lower())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "fef13878-c8fa-4d63-bb1d-31be9fddcb66",
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
       "      <th>QuestionID</th>\n",
       "      <th>Category</th>\n",
       "      <th>QuestionType</th>\n",
       "      <th>QuestionTime</th>\n",
       "      <th>chunk_index</th>\n",
       "      <th>chunk_text</th>\n",
       "      <th>search_text</th>\n",
       "      <th>lexical_tokens</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>row_0_chunk_0</td>\n",
       "      <td>C15Q2112</td>\n",
       "      <td>Tools and Home Improvement</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2013-04-20</td>\n",
       "      <td>0</td>\n",
       "      <td>dimensions item</td>\n",
       "      <td>Tools and Home Improvement open-ended dimensio...</td>\n",
       "      <td>[tools, and, home, improvement, open, ended, d...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>row_1_chunk_0</td>\n",
       "      <td>C9Q4595</td>\n",
       "      <td>Home and Kitchen</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-02-06</td>\n",
       "      <td>0</td>\n",
       "      <td>much booze hold poured booze measuring cup sun...</td>\n",
       "      <td>Home and Kitchen open-ended much booze hold po...</td>\n",
       "      <td>[home, and, kitchen, open, ended, much, booze,...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>row_2_chunk_0</td>\n",
       "      <td>C4Q7999</td>\n",
       "      <td>Cell Phones and Accessories</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-08-09</td>\n",
       "      <td>0</td>\n",
       "      <td>case fit nokia lumia 520 yes fits great great ...</td>\n",
       "      <td>Cell Phones and Accessories open-ended case fi...</td>\n",
       "      <td>[cell, phones, and, accessories, open, ended, ...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>row_3_chunk_0</td>\n",
       "      <td>C8Q8916</td>\n",
       "      <td>Health and Personal Care</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2014-04-25</td>\n",
       "      <td>0</td>\n",
       "      <td>folded sitting position high ground seat 30 in...</td>\n",
       "      <td>Health and Personal Care open-ended folded sit...</td>\n",
       "      <td>[health, and, personal, care, open, ended, fol...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>row_4_chunk_0</td>\n",
       "      <td>C14Q905</td>\n",
       "      <td>Sports and Outdoors</td>\n",
       "      <td>open-ended</td>\n",
       "      <td>2015-04-15</td>\n",
       "      <td>0</td>\n",
       "      <td>long leave get max sweat benefit keep thinking...</td>\n",
       "      <td>Sports and Outdoors open-ended long leave get ...</td>\n",
       "      <td>[sports, and, outdoors, open, ended, long, lea...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "        chunk_id QuestionID                     Category QuestionType  \\\n",
       "0  row_0_chunk_0   C15Q2112   Tools and Home Improvement   open-ended   \n",
       "1  row_1_chunk_0    C9Q4595             Home and Kitchen   open-ended   \n",
       "2  row_2_chunk_0    C4Q7999  Cell Phones and Accessories   open-ended   \n",
       "3  row_3_chunk_0    C8Q8916     Health and Personal Care   open-ended   \n",
       "4  row_4_chunk_0    C14Q905          Sports and Outdoors   open-ended   \n",
       "\n",
       "  QuestionTime  chunk_index  \\\n",
       "0   2013-04-20            0   \n",
       "1   2014-02-06            0   \n",
       "2   2014-08-09            0   \n",
       "3   2014-04-25            0   \n",
       "4   2015-04-15            0   \n",
       "\n",
       "                                          chunk_text  \\\n",
       "0                                    dimensions item   \n",
       "1  much booze hold poured booze measuring cup sun...   \n",
       "2  case fit nokia lumia 520 yes fits great great ...   \n",
       "3  folded sitting position high ground seat 30 in...   \n",
       "4  long leave get max sweat benefit keep thinking...   \n",
       "\n",
       "                                         search_text  \\\n",
       "0  Tools and Home Improvement open-ended dimensio...   \n",
       "1  Home and Kitchen open-ended much booze hold po...   \n",
       "2  Cell Phones and Accessories open-ended case fi...   \n",
       "3  Health and Personal Care open-ended folded sit...   \n",
       "4  Sports and Outdoors open-ended long leave get ...   \n",
       "\n",
       "                                      lexical_tokens  \n",
       "0  [tools, and, home, improvement, open, ended, d...  \n",
       "1  [home, and, kitchen, open, ended, much, booze,...  \n",
       "2  [cell, phones, and, accessories, open, ended, ...  \n",
       "3  [health, and, personal, care, open, ended, fol...  \n",
       "4  [sports, and, outdoors, open, ended, long, lea...  "
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# Tokenize Lexical Documents\n",
    "# =============================================================================\n",
    "lexical_dataset[\"lexical_tokens\"] = (lexical_dataset[\"search_text\"].fillna(\"\").apply(tokenize_text))\n",
    "lexical_dataset.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "id": "8cac2e60-a3ee-437b-a3df-e4b99e2762e0",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['tools', 'and', 'home', 'improvement', 'open', 'ended', 'dimensions', 'item']\n"
     ]
    }
   ],
   "source": [
    "print(lexical_dataset.loc[0, \"lexical_tokens\"])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "id": "748004f0-c692-4ea2-8fd8-d5167e3961d2",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Embeddings saved successfully.\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# Save embedding matrix\n",
    "# =============================================================================\n",
    "np.save(\"semantic_embeddings.npy\", embeddings)\n",
    "print(\"Embeddings saved successfully.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "id": "d823f8da-c523-4057-a270-33292bcc8c83",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Semantic dataset saved successfully.\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# Save Metadata of semantic dataset\n",
    "# =============================================================================\n",
    "semantic_dataset.to_csv(\"semantic_chunks.csv\",index=False)\n",
    "print(\"Semantic dataset saved successfully.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "id": "d24802a4-a31f-47da-9621-84be15f029ba",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Lexical dataset saved successfully.\n"
     ]
    }
   ],
   "source": [
    "# =============================================================================\n",
    "# Save Lexical Dataset for BM25\n",
    "# =============================================================================\n",
    "lexical_dataset.to_csv(\"lexical_tokens.csv\", index=False)\n",
    "print(\"Lexical dataset saved successfully.\")"
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
