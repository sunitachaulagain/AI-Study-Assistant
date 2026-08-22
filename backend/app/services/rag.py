from backend.app.services.retrieval import retrieve_chunks
from backend.app.services.local_llm import generate_answer


def answer_question(
    question: str,
    top_k: int = 5
) -> str:

    # Retrieve relevant chunks
    chunks = retrieve_chunks(
        question,
        top_k=top_k
    )

    if not chunks:
        return "I could not find relevant information in the provided documents."

    # Combine retrieved chunks into context
    context_parts = []

    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[Source {i}]\n{chunk.content}"
        )

    context = "\n\n".join(context_parts)

    # Generate answer using local LLM
    answer = generate_answer(
        question=question,
        context=context
    )

    return answer


if __name__ == "__main__":

    question = "What are the main causes of road accidents in Nepal?"

    print("\nQuestion:")
    print(question)

    print("\nGenerating answer...")

    answer = answer_question(question)

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(answer)