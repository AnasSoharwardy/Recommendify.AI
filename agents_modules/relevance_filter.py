from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_groq import ChatGroq

def _get_llm(model_name: str = "llama3-8b-8192") -> Runnable:
    return ChatGroq(model=model_name, temperature=0.0)

def build_agent(system_prompt: str, user_prompt: str, output_format: str) -> Runnable:
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", f"{user_prompt}\n\nRespond ONLY in this format:\n{output_format}")
    ])
    return prompt | _get_llm()

def build_relevance_agent() -> Runnable:
    system_prompt = "You are a strict video relevance evaluator."
    user_prompt = (
        "Product: {product}\n"
        "Video Title: {title}\n"
        "Transcript Snippet:\n{snippet}\n\n"
        "Determine if this video is a review of the specified product."
    )
    output_format = '{{"is_review": "Yes" | "No"}}'
    return build_agent(system_prompt, user_prompt, output_format)

def relevance_filter(product: str, videos: list[dict]) -> list[dict]:
    agent = build_relevance_agent()
    relevant = []

    for vid in videos:
        snippet = vid["transcript"][:5000]

        print("\nChecking video:", vid["title"])
        print("Transcript snippet:", snippet[:200], "...\n")

        result = agent.invoke({
            "product": product,
            "title": vid["title"],
            "snippet": snippet
        }).content.strip()

        print("LLM response:", result)

        if "Yes" in result:
            relevant.append(vid)
        if len(relevant) == 5:
            break

    return relevant
