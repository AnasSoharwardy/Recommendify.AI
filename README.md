# 🤖 Recommendify.AI — AI-Powered YouTube Product Review Analyzer

Tired of watching 10 different YouTube reviews before buying one product?

Recommendify.ai is an AI-based product review assistant that saves you time and helps you make smarter buying decisions.  
Just enter a product name, and our system:

✅ Searches for the top YouTube video reviews  
✅ Filters out irrelevant videos and content  
✅ Extracts pros and cons from transcripts  
✅ Aggregates the insights  
✅ Gives you a final verdict (Recommended / Not Recommended)  

---

## How It Works (Multi-Agent Pipeline)

This project uses a LangGraph-powered multi-agent workflow to simulate the decision-making of an AI assistant.

### Agents Involved:

### 1. Product Specificity Checker  
   - Ensures the product query is specific (e.g., "Samsung Galaxy S25" instead of just "Samsung")

### 2. YouTube Search Agent  
   - Fetches top 10 YouTube video IDs using youtube-search-python API

### 3. YouTube Transcript Agent  
   - Extracts the transcript of videos using the YouTubeTranscriptAPI

### 4. Relevance Filter  
   - Uses an LLM (Groq) to filter out unrelated and irrelevant videos

### 5. Transcript Summarizer  
   - Extracts pros & cons from each transcript using LLM prompting

### 6. Verdict Aggregator  
   - Aggregates pros/cons across all videos and generates a final recommendation along with reasoning

---
## How to Run

### 1. Install Dependencies

```
pip install -r requirements.txt
```

### 2. Add Your Groq API Key

Edit the `.env` file in the root directory and replace it with your key:

```
GROQ_API_KEY = your_groq_api_key
```

You can get the GROQ API KEY from [here](https://console.groq.com/keys)

### 4. Run the Tool

Run the provided file to automatically launch the tool
```
RUN ME.bat
```

Or manually open 2 terminals and enter the following:

In the first terminal:

```
uvicorn main:app --reload
```

In the second terminal:

```
streamlit run app.py
```

Then go to:  
`http://localhost:8501`

---
## Tech Stack

- LangGraph + LangChain
- LLMs via Groq API
- Python 3.10+
- FastAPI (Backend)
- Streamlit (Frontend)
- YouTube APIs

---
