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

def build_verdict_agent():
    system_prompt = "You are an expert product analyst and sentiment evaluator."
    user_prompt = (
        "Product: {product}\n\n"
        "Here are summaries of 5 YouTube reviews for this product, each containing pros and cons:\n\n"
        "{summaries}\n\n"
        "Only from the provided summaries; Analyze the pros and cons and determine whether this product should be recommended or not."
    )
    output_format = (
        '{{"recommendation": "Recommended" | "Not Recommended", '
        '"reason": "Concise explanation based on the reviews"}}'
    )
    return build_agent(system_prompt, user_prompt, output_format)

def aggregate_verdict(product: str, summaries: list[dict]) -> dict:
    
    if not summaries:
        print("Final Verdict: No reviews found")
        return "No reviews found"
    
    agent = build_verdict_agent()

    combined = "\n\n".join(
        f"Video {i+1} - {s['title']}:\n{s['summary']}" for i, s in enumerate(summaries)
    )

    result = agent.invoke({
        "product": product,
        "summaries": combined
    }).content.strip()

    print("Final Verdict:", result)
    return result
