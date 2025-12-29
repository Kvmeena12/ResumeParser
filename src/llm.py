from langchain_groq import ChatGroq


def load_llm(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.15,
    max_tokens=3000
):
    return ChatGroq(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format={"type": "json_object"}
    )

def load_text_llm(
    model: str = "meta-llama/llama-4-scout-17b-16e-instruct",
    temperature: float = 0.5,        # human-like language
    max_tokens: int = 1200
):
    return ChatGroq(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens
    )
