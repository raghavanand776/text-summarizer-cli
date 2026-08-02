import os
import sys
from pathlib import Path

from anthropic import Anthropic
from anthropic import APIConnectionError, APIError, APIStatusError, RateLimitError
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

word_count = len(text.split())
estimated_input_tokens = word_count * 1.3
estimated_input_cost = estimated_input_tokens / 1_000_000 * 1
estimated_output_cost = 200 / 1_000_000 * 5
estimated_total_cost = estimated_input_cost + estimated_output_cost

print(
    f"Estimated cost: ${estimated_total_cost:.6f} "
    f"(approx. {estimated_input_tokens:.0f} input tokens, 200 output tokens)"
)

try:
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
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    actual_input_cost = input_tokens / 1_000_000 * 1
    actual_output_cost = output_tokens / 1_000_000 * 5
    actual_total_cost = actual_input_cost + actual_output_cost

    print(f"Actual input tokens: {input_tokens}")
    print(f"Actual output tokens: {output_tokens}")
    print(f"Actual cost: ${actual_total_cost:.6f}")
except (APIConnectionError, APIError, APIStatusError, RateLimitError) as exc:
    print("Sorry, I couldn't complete the summary request right now.")
    print(f"Anthropic API error: {exc}")
    print("Please check your API key, your network connection, or try again later.")
