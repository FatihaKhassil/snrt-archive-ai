class PromptBuilder:

    @staticmethod
    def build(
        text
    ):

        return f"""
You are an AI assistant.

Analyze the following document.

IMPORTANT:

- Detect the language of the document.
- Keep the SAME language as the original document.
- Do NOT translate the content.
- Generate a concise summary.
- Extract the most relevant keywords.
- Return ONLY a valid JSON object.
- Do NOT write explanations.
- Do NOT write Markdown.
- Do NOT use ```json.
- Do NOT write any text before or after the JSON.

The JSON format must be:

{{
    "summary": "...",
    "keywords": [
        "...",
        "...",
        "..."
    ]
}}

Document:

{text}
"""