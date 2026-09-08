from backend.app.services.retrieval import retrieve_chunks
from backend.app.services.local_llm import generate_answer


def answer_question(
    question: str,
    user_id: int,
    top_k: int = 5
) -> str:

    # Retrieve relevant chunks only from the current user's documents
    chunks = retrieve_chunks(
        question,
        user_id=user_id,
        top_k=top_k
    )

    if not chunks:
        return "I could not find relevant information in your documents."

    # Combine retrieved chunks into context
    context_parts = []

    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[Source {i}]\n{chunk.content}"
        )

    context = "\n\n".join(context_parts)

    # Generate answer using the local LLM
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

    # For direct testing, use an existing user ID
    answer = answer_question(
        question=question,
        user_id=3
    )

    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(answer)