import logging

from backend.app.services.retrieval import retrieve_chunks
from backend.app.services.local_llm import generate_answer

logger = logging.getLogger(__name__)


def answer_question(
    question: str,
    user_id: int,
    top_k: int = 5,
    subject_id: int = None
) -> str:

    logger.info(f"answer_question: user_id={user_id}, subject_id={subject_id}, question={question[:80]}")

    # Retrieve relevant chunks only from the current user's documents
    chunks = retrieve_chunks(
        question,
        user_id=user_id,
        top_k=top_k,
        subject_id=subject_id
    )

    logger.info(f"Retrieved {len(chunks)} chunks")

    if not chunks:
        return "I could not find relevant information in your documents."

    # Combine retrieved chunks into context
    context_parts = []

    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[Source {i}]\n{chunk.content}"
        )

    context = "\n\n".join(context_parts)

    # Limit context to prevent oversized prompts
    max_context_chars = 2000
    if len(context) > max_context_chars:
        context = context[:max_context_chars] + "\n[...truncated...]"

    logger.info(f"Context length: {len(context)} chars")

    # Generate answer using the local LLM
    answer = generate_answer(
        question=question,
        context=context
    )

    logger.info(f"Answer length: {len(answer)} chars")

    return answer


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    question = "What are the main causes of road accidents in Nepal?"

    logger.info(f"Question: {question}")

    answer = answer_question(
        question=question,
        user_id=3
    )

    logger.info(f"Answer: {answer}")