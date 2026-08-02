import os
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()

if len(sys.argv) > 1:
    input_value = sys.argv[1]
    if Path(input_value).exists():
        with open(input_value, "r", encoding="utf-8") as handle:
            text = handle.read()
    else:
        text = input_value
else:
    text = sys.stdin.read()

if len(text) > 10000:
    print("Input too long. Please provide text shorter than 10,000 characters.")
    sys.exit()

for proxy_var in (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
):
    os.environ.pop(proxy_var, None)

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=200,
    temperature=0.2,
    messages=[
        {
            "role": "user",
            "content": (
                "Summarize this text in 2-3 sentences maximum, "
                "focused on the single most important point.\n\n"
                f"{text}"
            ),
        }
    ],
)

print(response.content[0].text)
