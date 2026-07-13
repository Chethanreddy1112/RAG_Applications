# Bank of America Credit Card RAG System

A Retrieval-Augmented Generation (RAG) application that crawls Bank of America credit card information, indexes it into a Chroma vector database, and answers user queries using an LLM.

---

## Project Overview

This project performs the following tasks:

- Crawls Bank of America credit card information.
- Extracts card details such as:
  - Card Name
  - Category
  - Features
  - Benefits
  - Rates & Fees
- Cleans and chunks the data.
- Creates embeddings using HuggingFace.
- Stores embeddings in ChromaDB.
- Retrieves relevant information using semantic search.
- Generates accurate answers using an LLM (Groq/OpenRouter).
- Provides an interactive Streamlit interface.

---

## Tech Stack

- Python
- Crawl4AI
- BeautifulSoup
- LangChain
- HuggingFace Embeddings
- ChromaDB
- Groq / OpenRouter
- Streamlit

---

## Project Structure

```
RAG/
│
├── crawler.py
├── preprocess.py
├── index.py
├── rag_api.py
├── app.py
├── requirements.txt
│
├── scraped_data/
│   ├── cards.json
│   └── chunks.json
│
├── chroma_db/
│
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd RAG
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# API Key Setup

If using **Groq**, create a `.env` file.

```
GROQ_API_KEY=your_api_key
```

If using **OpenRouter**

```
OPENROUTER_API_KEY=your_api_key
```

---

# Running the Project

## Step 1: Crawl Data

Run:

```bash
python crawler.py
```

Output:

```
scraped_data/cards.json
```

---

## Step 2: Preprocess Data

Run:

```bash
python preprocess.py
```

This script:

- Cleans the scraped data
- Splits text into chunks
- Saves chunks into

```
scraped_data/chunks.json
```

---

## Step 3: Create Vector Database

Run:

```bash
python index.py
```

This will:

- Load embedding model
- Convert chunks into embeddings
- Store vectors inside ChromaDB

Output:

```
chroma_db/
```

---

## Step 4: Run the Application

```bash
streamlit run app.py
```

The application opens at

```
http://localhost:8501
```

---

# Project Workflow

```
Bank of America Website
            │
            ▼
       crawler.py
            │
            ▼
       cards.json
            │
            ▼
     preprocess.py
            │
            ▼
      chunks.json
            │
            ▼
        index.py
            │
            ▼
       Chroma Vector DB
            │
            ▼
        rag_api.py
            │
            ▼
        Streamlit UI
            │
            ▼
     AI Generated Answer
```

---

# Example Queries

- What travel rewards do Bank of America cards offer?
- Which credit card has no annual fee?
- What are the benefits of the Travel Rewards Credit Card?
- Compare the Travel Rewards card with the Cash Rewards card.
- Which credit card is suitable for students?
- Which cards offer cashback?
- What are the introductory APR offers?
- Which cards have no foreign transaction fees?
- Which credit card helps build credit?
- What are the features of the Premium Rewards card?

---

# Example Output

### User

```
What travel rewards do Bank of America cards offer?
```

### AI Answer

```
The Bank of America® Travel Rewards Credit Card offers:

• Unlimited travel reward points on every purchase.
• No foreign transaction fees.
• No annual fee.
• Introductory bonus points after eligible purchases.
```

### Sources

```
Bank of America® Travel Rewards Credit Card

https://www.bankofamerica.com/credit-cards/products/travel-rewards-credit-card/
```

---

# Technologies Used

| Component | Technology |
|----------|-------------|
| Language | Python |
| Scraping | Crawl4AI, BeautifulSoup |
| Text Splitting | LangChain |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Vector Database | ChromaDB |
| LLM | Groq / OpenRouter |
| UI | Streamlit |

---

# Future Improvements

- Crawl additional Bank of America product pages.
- Improve extraction of APR and fees.
- Add citation highlighting.
- Support multiple banking websites.
- Implement conversational memory.
- Deploy using Render or Streamlit Community Cloud.

---

# Author

**Chethan Reddy**

B.Tech CSE (AI & ML)

CMR Technical Campus