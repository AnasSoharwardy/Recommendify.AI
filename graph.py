# graph.py

from typing import TypedDict, Optional, List, Dict
from langgraph.graph import StateGraph, END


from agents_modules.product_checker import product_checker
from agents_modules.youtube_search import youtube_search
from agents_modules.transcript_fetcher import fetch_transcripts
from agents_modules.relevance_filter import relevance_filter
from agents_modules.transcript_summarizer import summarize_transcripts
from agents_modules.verdict_aggregator import aggregate_verdict


class GraphState(TypedDict):
    query: Optional[str]
    product_type: Optional[str]
    video_ids: Optional[List[str]]
    transcripts: Optional[List[Dict]]
    relevant_videos: Optional[List[Dict]]
    summaries: Optional[List[Dict]]
    verdict: Optional[str]
    error: Optional[str]


# Node 1: Product specificity check
def run_product_checker(state: GraphState) -> dict:
    result = product_checker(state["query"])
    state["product_type"] = result

    if result == "Specific":
        return state | {"next": "valid"}
    else:
        state["error"] = (
            "The product is too generic. Please enter a more specific product with its model"
            "(e.g., Sony PS5)."
        )
        return state | {"next": "error"}


# Node 2: YouTube Search
def run_youtube_search(state: GraphState) -> GraphState:
    ids = youtube_search(state["query"])
    state["video_ids"] = ids
    return state


# Node 3: Fetch transcripts
def run_transcript_fetcher(state: GraphState) -> GraphState:
    tx = fetch_transcripts(state["video_ids"])
    state["transcripts"] = tx
    return state


# Node 4: Filter relevant videos
def run_relevance_filter(state: GraphState) -> GraphState:
    relevant = relevance_filter(state["query"], state["transcripts"])
    state["relevant_videos"] = relevant
    return state


# Node 5: Summarize transcripts
def run_summarizer(state: GraphState) -> GraphState:
    summaries = summarize_transcripts(state["query"], state["relevant_videos"])
    state["summaries"] = summaries
    return state


# Node 6: Final verdict
def run_verdict(state: GraphState) -> GraphState:
    result = aggregate_verdict(state["query"], state["summaries"])
    state["verdict"] = result
    return state


# Build LangGraph
def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("product_check", run_product_checker)
    workflow.add_node("youtube_search", run_youtube_search)
    workflow.add_node("transcript_fetcher", run_transcript_fetcher)
    workflow.add_node("relevance_filter", run_relevance_filter)
    workflow.add_node("summarizer", run_summarizer)
    workflow.add_node("verdict", run_verdict)
    
    workflow.set_entry_point("product_check")
   
    workflow.add_conditional_edges(
        "product_check",
        lambda output: output["next"],
        {
            "valid": "youtube_search",
            "error": END,
        },
    )
    
    workflow.add_edge("youtube_search", "transcript_fetcher")
    workflow.add_edge("transcript_fetcher", "relevance_filter")
    workflow.add_edge("relevance_filter", "summarizer")
    workflow.add_edge("summarizer", "verdict")
    workflow.add_edge("verdict", END)

    return workflow.compile()
