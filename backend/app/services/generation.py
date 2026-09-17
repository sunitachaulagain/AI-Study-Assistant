from backend.app.services.local_llm import generate_text


def generate_answer(question, context):

    prompt = f"""You are an AI study assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

    return generate_text(
        prompt,
        max_new_tokens=300
    )