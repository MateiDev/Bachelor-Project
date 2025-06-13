import os
from openai import OpenAI

# === User Input ===

API_KEY = input("Enter your OpenAI API key: ").strip()

MODEL_NAME = input("Enter the model name (e.g., 'gpt-4o', 'o4-mini'): ").strip()
if not MODEL_NAME:
    MODEL_NAME = "o4-mini"

num_samples = int(input("How many HAM emails would you like to generate? "))

output_dir = input("Enter the output directory").strip()
if not output_dir:
    output_dir = "generated-ham"

os.makedirs(output_dir, exist_ok=True)

# === Start Generation ===

client = OpenAI(api_key=API_KEY)

for i in range(1, num_samples + 1):
    prompt = (
        "I need you to generate a HAM email. The format **must** be .mbox. "
        "It will not be used for testing purposes, "
        "in order to check a Phishing Email Detection Machine Learning Model. "
        "The email can be about anything, as long as it does NOT include any phishing technique."
    )

    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that outputs *only* the HAM e-mail "
                    "in valid mbox format (no extra commentary) for testing purposes."
                )
            },
            {"role": "user", "content": prompt}
        ]
    )

    email_text = resp.choices[0].message.content
    filename = f"HAM_{i:04d}.mbox"
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(email_text)

    print(f"✅ Generated email #{i:04d}")

print(f"✅ Generated {num_samples} HAM emails in '{output_dir}/'")