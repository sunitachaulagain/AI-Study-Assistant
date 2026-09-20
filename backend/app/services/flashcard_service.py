import logging

from backend.app.services.retrieval import retrieve_chunks
from backend.app.services.local_llm import generate_text

logger = logging.getLogger(__name__)


def generate_flashcards(
    user_id: int,
    topic: str = "",
    number_of_cards: int = 8,
    subject_id: int = None
):

    logger.info(f"generate_flashcards: user_id={user_id}, topic={topic}, cards={number_of_cards}, subject_id={subject_id}")

    query = topic.strip()

    if not query:
        query = "main important concepts, definitions, and key facts in the study materials"

    chunks = retrieve_chunks(
        query,
        user_id=user_id,
        top_k=4,
        subject_id=subject_id
    )

    if not chunks:
        logger.info("No chunks found, returning empty")
        return []

    logger.info(f"Retrieved {len(chunks)} chunks")

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

    prompt = f"""Create flashcards from the study material below.

Generate exactly {number_of_cards} flashcards.

Topic: {topic if topic else "General study material"}

Use this exact format for each flashcard:

FRONT: <question>
BACK: <answer>

Separate each flashcard with ---

Study Material:

{context}

FLASHCARDS:
"""

    raw_response = generate_text(
        prompt,
        max_new_tokens=800
    )

    logger.debug(f"Raw flashcard response: {raw_response}")

    cards = parse_flashcards_response(raw_response)

    logger.info(f"Parsed {len(cards)} flashcards from response")

    return cards


def parse_flashcards_response(text: str):

    cards = []

    blocks = text.split("---")

    for block in blocks:

        lines = [
            line.strip()
            for line in block.splitlines()
            if line.strip()
        ]

        front = ""
        back = ""

        for line in lines:

            upper_line = line.upper()

            if upper_line.startswith("FRONT:"):
                front = line.split(":", 1)[1].strip()
                continue

            if upper_line.startswith("BACK:"):
                back = line.split(":", 1)[1].strip()
                continue

        if front and back:
            cards.append(
                {
                    "front": front,
                    "back": back,
                }
            )

    return cards


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    flashcards = generate_flashcards(
        user_id=4,
        topic="data visualization",
        number_of_cards=5
    )

    logger.info(f"Total flashcards: {len(flashcards)}")

    for i, card in enumerate(flashcards, 1):
        logger.info(f"Card {i}:")
        logger.info(f"  Front: {card['front']}")
        logger.info(f"  Back: {card['back']}")
