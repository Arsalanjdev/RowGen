def trim_code_block(text: str, language: str = "") -> str:
    """
    Removes markdown code block fences like ```json ... ```
    """
    prefix = f"```{language}" if language else "```"

    if text.startswith(prefix):
        text = text.removeprefix(prefix).strip()
    elif text.startswith("```"):
        text = text.removeprefix("```").strip()

    if text.endswith("```"):
        text = text.removesuffix("```").strip()

    return text


def parse_sql_from_code_block(text: str) -> str:
    """
    Return cleaned SQL query string
    """
    return trim_code_block(text, "sql")
