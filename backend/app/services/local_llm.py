import logging

import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

logger = logging.getLogger(__name__)

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


logger.info("Loading local LLM...")

if torch.cuda.is_available():
    gpu_name = torch.cuda.get_device_name(0)
    gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    logger.info(f"GPU detected: {gpu_name} ({gpu_mem:.1f} GB)")
    device_map = "auto"
    torch_dtype = torch.float16
else:
    logger.info("No GPU detected, using CPU")
    device_map = None
    torch_dtype = torch.float32

generator = pipeline(
    "text-generation",
    model=MODEL_NAME,
    device_map=device_map,
    torch_dtype=torch_dtype,
    max_length=None,
)

logger.info("Local LLM loaded successfully.")


def generate_text(
    prompt: str,
    max_new_tokens: int = 200
) -> str:

    logger.debug("Generating response...")

    result = generator(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        return_full_text=False,
    )

    logger.debug("Generation completed.")

    return result[0]["generated_text"].strip()


def generate_answer(
    question: str,
    context: str
) -> str:

    prompt = f"""You are a helpful AI study assistant. Answer the student's question based on the study material provided below.

Use the information from the study material to give a clear, complete, and helpful answer. If the study material contains relevant information, always use it to answer — do not refuse if the answer can be found or reasonably inferred from the context.

Only say "I could not find the answer in the provided documents" if the study material is completely unrelated to the question.

Study Material:
{context}

Question:
{question}

Answer:
"""

    return generate_text(
        prompt,
        max_new_tokens=200
    )