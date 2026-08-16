from pypdf import PdfReader
import re


def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())

    return text


def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    return sentences


def chunk_text(sentences, chunk_size=500, overlap=100):
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:

        # Handle sentences larger than chunk_size
        if len(sentence) > chunk_size:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0

            step = chunk_size - overlap

            for i in range(0, len(sentence), step):
                chunk = sentence[i:i + chunk_size]
                chunks.append(chunk)

            continue

        # Add sentence to current chunk
        if current_length + len(sentence) > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))

            # Create overlap from previous sentences
            overlap_text = []
            overlap_length = 0

            for previous_sentence in reversed(current_chunk):
                if overlap_length + len(previous_sentence) > overlap:
                    break

                overlap_text.insert(0, previous_sentence)
                overlap_length += len(previous_sentence)

            current_chunk = overlap_text
            current_length = overlap_length

        current_chunk.append(sentence)
        current_length += len(sentence)

    # Add remaining sentences
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


file_path = "uploads/AI_for_Road_Safety_in_Nepal_Reviewed.pdf"

reader = PdfReader(file_path)

all_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        all_text += text + "\n"


cleaned_text = clean_text(all_text)

sentences = split_sentences(cleaned_text)

chunks = chunk_text(
    sentences,
    chunk_size=500,
    overlap=100
)
print("\nChunk sizes:")

for i, chunk in enumerate(chunks[:10]):
    print(f"Chunk {i}: {len(chunk)} characters")


print("Original characters:", len(all_text))
print("Cleaned characters:", len(cleaned_text))
print("Number of sentences:", len(sentences))
print("Number of chunks:", len(chunks))


print("\nFirst 5 sentences:")

for sentence in sentences[:5]:
    print("\n---")
    print(sentence)


print("\nFirst chunk:")
print(chunks[0])

print("\nSecond chunk:")
print(chunks[1])