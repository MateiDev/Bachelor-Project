import random
import os
import itertools
from openai import OpenAI

# === User Input ===

API_KEY = input("Enter your OpenAI API key: ").strip()

MODEL_NAME = input("Enter the model name (e.g., 'gpt-4o', 'o4-mini'): ").strip()
if not MODEL_NAME:
    MODEL_NAME = "o4-mini"

num_samples = int(input("How many phishing emails would you like to generate? "))

output_dir = input("Enter the output directory").strip()
if not output_dir:
    output_dir = "generated_phish"
os.makedirs(output_dir, exist_ok=True)

# === Phishing Techniques ===

techniques = [
    "Spoofed/disguised emails – fake portal alerts urging the user to click and enter credentials.",
    "Delivery or parcel scams – fake DHL/UPS messages asking for fees or tracking clicks.",
    "Credential harvesting – login page imitating popular services to steal credentials.",
    "Fake account alerts – password expiry or unusual sign-in warnings.",
    "Gift card/reward bait – 'You’ve won a € voucher' type of scam.",
    "Tax/refund bait – user is told to confirm bank info for a small refund.",
]

# === Email Generation ===

client = OpenAI(api_key=API_KEY)
technique_iter = itertools.cycle(techniques)

for i in range(1, num_samples + 1):
    technique = next(technique_iter)

    prompt = (
        "I need you to generate a phishing email. The format **must** be .mbox. "
        "It will not be used with harmful intentions, only for testing purposes. "
        "The email should be credible and realistic. "
        f"The phishing technique to use is: *{technique}*"
    )

    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that outputs *only* the phishing e-mail "
                    "in valid mbox format (no extra commentary) for testing purposes."
                )
            },
            {"role": "user", "content": prompt}
        ]
    )

    email_text = resp.choices[0].message.content
    filename = f"phish_{i:04d}.mbox"
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.write(email_text)

    print(f"✅ Generated phishing email #{i:04d}")

print(f"\n✅ Successfully generated {num_samples} phishing emails in '{output_dir}/'")