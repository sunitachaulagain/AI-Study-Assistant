from transformers import pipeline


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


print("Loading local LLM...")

generator = pipeline(
    "text-generation",
    model=MODEL_NAME,
    device=-1,  # CPU
)

print("Local LLM loaded successfully.")


def generate_answer(question: str, context: str) -> str:

    prompt = f"""You are an AI study assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided documents."

Do not invent information.

Context:
{context}

Question:
{question}

Answer:
"""

    result = generator(
        prompt,
        max_new_tokens=200,
        do_sample=False,
    )

    generated_text = result[0]["generated_text"]

    return generated_text[len(prompt):].strip()


if __name__ == "__main__":

    answer = generate_answer(
        "What are the main causes of road accidents in Nepal?",
        """
        Road accidents in Nepal are influenced by heavy traffic,
        poor road infrastructure, variable weather conditions,
        narrow roads, unpredictable weather, and poor road conditions.
        """
    )

    print("\nGenerated answer:")
    print(answer)