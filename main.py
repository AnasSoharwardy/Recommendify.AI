from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph import build_graph
import uvicorn
from dotenv import load_dotenv
import os

# Enter api key in .env

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Allow Streamlit frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.post("/analyze")
async def analyze_product(req: QueryRequest):
    query = req.query.strip()
    graph = build_graph()

    try:
        final_state = graph.invoke({"query": query})

        # Case: product is too generic
        if final_state.get("error"):
            return {
                "success": False,
                "error": final_state["error"]
            }

        # Case: success
        return {
            "success": True,
            "verdict": final_state["verdict"],
            "video_count": len(final_state.get("relevant_videos", [])),
            "summaries": final_state.get("summaries", [])
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)

# Or run in terminal via: uvicorn main:app --reload
