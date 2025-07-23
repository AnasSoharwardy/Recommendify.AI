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

def product_checker(query: str) -> str:
    system_prompt = (
        "You are part of a Multi Agent System that provides review of various products. "
        "Your job is to check whether the query entered by user is a specific product or not."
    )
    user_prompt = (
        "Determine whether the following query refers to ONE specific product "
        "or a GENERIC product category. Make sure the query mentions a product model.\n\n"
        "Query: {query}"
    )
    output_format = '{{"answer": "Specific" | "Generic"}}'

    chain = build_agent(system_prompt, user_prompt, output_format)
    result = chain.invoke({"query": query}).content.strip().lower()
    return "Specific" if "specific" in result else "Generic"
