import logging

from backend.app.services.retrieval import retrieve_chunks
from backend.app.services.local_llm import generate_text

logger = logging.getLogger(__name__)


def generate_quiz(
    user_id: int,
    topic: str = "",
    number_of_questions: int = 5,
    subject_id: int = None
):

    query = topic.strip()

    if not query:
        query = "main important concepts and topics in the study materials"

    # Retrieve relevant study material
    chunks = retrieve_chunks(
        query,
        user_id=user_id,
        top_k=3,
        subject_id=subject_id
    )

    if not chunks:
        return []

    # Build context
    context_parts = []

    for i, chunk in enumerate(chunks, 1):
        context_parts.append(
            f"[Source {i}]\n{chunk.content}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""You are an AI study assistant.

Create a multiple-choice quiz using ONLY the study material below.

Generate exactly {number_of_questions} questions.

Topic: {topic if topic else "General study material"}

For each question use this format:

QUESTION: <question>

A) <option>
B) <option>
C) <option>
D) <option>

ANSWER: <A, B, C, or D>

EXPLANATION: <short explanation>

Rules:
- Use only information from the study material.
- Do not invent facts.
- Each question must have exactly four options.
- Only one option must be correct.
- Make incorrect options plausible.
- Do not repeat questions.
- Keep explanations short.
- Do not add extra headings.
- Make every question complete.

STUDY MATERIAL:

{context}

QUIZ:
"""

    raw_response = generate_text(
        prompt,
        max_new_tokens=400
    )

    logger.debug(f"Raw quiz response: {raw_response}")

    return parse_quiz_response(raw_response)


def parse_quiz_response(text: str):

    questions = []

    blocks = text.split("QUESTION:")

    for block in blocks[1:]:

        lines = [
            line.strip()
            for line in block.splitlines()
            if line.strip()
        ]

        question = ""
        options = []
        correct_answer = None
        explanation = ""

        parsing_explanation = False

        for line in lines:

            upper_line = line.upper()

            # -------------------------------------------------
            # Ignore headings
            # -------------------------------------------------

            if upper_line == "OPTIONS:":
                parsing_explanation = False
                continue

            # -------------------------------------------------
            # Stop if another question appears
            # -------------------------------------------------

            if upper_line.startswith("QUESTION:"):
                break

            # -------------------------------------------------
            # Options
            # Supports:
            # A) text
            # A. text
            # OPTION A: text
            # OPT A: text
            # -------------------------------------------------

            if (
                upper_line.startswith("OPTION A:")
                or upper_line.startswith("OPT A:")
            ):
                options.append(
                    line.split(":", 1)[1].strip()
                )
                parsing_explanation = False
                continue

            if (
                upper_line.startswith("OPTION B:")
                or upper_line.startswith("OPT B:")
            ):
                options.append(
                    line.split(":", 1)[1].strip()
                )
                parsing_explanation = False
                continue

            if (
                upper_line.startswith("OPTION C:")
                or upper_line.startswith("OPT C:")
            ):
                options.append(
                    line.split(":", 1)[1].strip()
                )
                parsing_explanation = False
                continue

            if (
                upper_line.startswith("OPTION D:")
                or upper_line.startswith("OPT D:")
            ):
                options.append(
                    line.split(":", 1)[1].strip()
                )
                parsing_explanation = False
                continue

            # A) / A. format
            if (
                len(line) >= 3
                and line[0].upper() in ["A", "B", "C", "D"]
                and line[1] in [")", "."]
            ):
                options.append(
                    line[2:].strip()
                )
                parsing_explanation = False
                continue

            # -------------------------------------------------
            # Answer
            #
            # Supports:
            # ANSWER: A
            # ANSWER: A)
            # ANSWER: A.
            # -------------------------------------------------

            if upper_line.startswith("ANSWER:"):

                answer = (
                    line.split(":", 1)[1]
                    .strip()
                    .upper()
                )

                # Remove punctuation produced by the LLM
                answer = answer.rstrip(").")

                answer_map = {
                    "A": 0,
                    "B": 1,
                    "C": 2,
                    "D": 3,
                }

                correct_answer = answer_map.get(answer)

                parsing_explanation = False
                continue

            # -------------------------------------------------
            # Explanation
            # -------------------------------------------------

            if upper_line.startswith("EXPLANATION:"):

                explanation = (
                    line.split(":", 1)[1]
                    .strip()
                )

                parsing_explanation = True
                continue

            # -------------------------------------------------
            # First normal line = question
            # -------------------------------------------------

            if not question and not parsing_explanation:
                question = line
                continue

            # -------------------------------------------------
            # Continue multiline explanation
            # -------------------------------------------------

            if parsing_explanation:
                explanation += " " + line

        # -----------------------------------------------------
        # Only accept complete questions
        # -----------------------------------------------------

        if (
            question
            and len(options) == 4
            and correct_answer is not None
        ):

            questions.append(
                {
                    "question": question,
                    "options": options,
                    "correct_answer": correct_answer,
                    "explanation": explanation,
                }
            )

    return questions


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    quiz = generate_quiz(
        user_id=4,
        topic="data visualization",
        number_of_questions=5
    )

    logger.info(f"Total questions: {len(quiz)}")

    for i, question in enumerate(quiz, 1):
        logger.info(f"Question {i}: {question['question']}")
        for j, option in enumerate(question["options"]):
            logger.info(f"  {chr(65 + j)}. {option}")
        logger.info(f"  Correct: {chr(65 + question['correct_answer'])}")
        logger.info(f"  Explanation: {question['explanation']}")