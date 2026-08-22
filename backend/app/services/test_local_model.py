from transformers import pipeline

model = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-1.5B-Instruct",
    device_map="auto",
)

messages = [
    {
        "role": "system",
        "content": "You are a helpful university study assistant."
    },
    {
        "role": "user",
        "content": "What is machine learning?"
    }
]

result = model(
    messages,
    max_new_tokens=150,
)

print(result[0]["generated_text"][-1]["content"])