from transformers import pipeline


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


generator = pipeline(
    "text-generation",
    model=MODEL_NAME,
    device_map="auto",
)


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

    result = generator(
        prompt,
        max_new_tokens=300,
        do_sample=False,
    )

    return result[0]["generated_text"]