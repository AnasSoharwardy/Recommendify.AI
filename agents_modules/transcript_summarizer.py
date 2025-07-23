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

def build_summary_agent():
    system_prompt = "You are a professional product review summarizer."
    user_prompt = (
        "The following is a YouTube video transcript reviewing a product.\n\n"
        "Product: {product}\n\n"
        "Transcript:\n{transcript}\n\n"
        "Your task is to extract a clear list of Pros and Cons from the transcript."
    )
    output_format = '{{"pros": [List of pros], "cons": [List of cons]}}'
    return build_agent(system_prompt, user_prompt, output_format)

def summarize_transcripts(product: str, relevant_videos: list[dict]) -> list[dict]:
    agent = build_summary_agent()
    summarized = []

    for vid in relevant_videos:
        print(f"\nSummarizing {vid['title']}...")

        result = agent.invoke({
            "product": product,
            "transcript": vid["transcript"][:4000]
        }).content.strip()

        print("Output:", result)

        if "pros" in result and "cons" in result:
            summarized.append({
                "id": vid["id"],
                "title": vid["title"],
                "summary": result
            })

    return summarized
