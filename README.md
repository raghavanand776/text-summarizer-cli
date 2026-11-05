# Text Summarizer CLI

A command-line tool that summarizes text with the Claude API, and tells you what each summary will cost before it runs.

My first project calling the Claude API directly. The goal was to learn the Messages API end to end and add the guardrails a real tool needs.

## What it does

- Takes text three ways: a **file path**, a **quoted string**, or **piped input** (`cat notes.txt | python3 summarizer.py`)
- Returns a 2–3 sentence summary focused on the single most important point
- Uses Claude Haiku for speed and low cost, with a low temperature (0.2) for consistent summaries

## Guardrails

| Guardrail | Why |
| --- | --- |
| **Input limit** (10,000 characters) | Stops oversized input before it costs anything |
| **Cost estimate before the call** | Approximates input tokens from word count and prints the expected cost |
| **Actual cost after the call** | Reads real token usage from the API response, so the estimate can be checked against reality |
| **Error handling** | Catches connection, rate-limit and API errors and prints a plain-language message instead of a stack trace |
| **Key stays local** | The API key is loaded from a `.env` file, which `.gitignore` keeps out of the repo |

## Run it

```bash
pip install anthropic python-dotenv
echo "ANTHROPIC_API_KEY=your-key-here" > .env

python3 summarizer.py sample_long.txt
python3 summarizer.py "Paste any text here to summarize it."
```

**Example output:**

```
Estimated cost: $0.000xxx (approx. NNN input tokens, 200 output tokens)
<2–3 sentence summary>
Actual input tokens: NNN
Actual output tokens: NN
Actual cost: $0.000xxx
```

## What I learned

- The shape of a Messages API call: model, max tokens, temperature, and the message list
- Estimating tokens before a call versus reading real usage after it
- Failing gracefully: a tool people rely on should explain what went wrong

Built with Claude Code as a pair programmer.
