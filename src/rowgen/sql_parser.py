def trim_code_block(text: str, language: str = "") -> str:
    """
    Removes markdown code block fences like ```sql ... ```
    and fixes SQLite-incompatible single quote escaping.
    """
    prefix = f"```{language}" if language else "```"

    if text.startswith(prefix):
        text = text.removeprefix(prefix).strip()
    elif text.startswith("```"):
        text = text.removeprefix("```").strip()

    if text.endswith("```"):
        text = text.removesuffix("```").strip()

    # Fix SQLite escaping
    text = text.replace("\\'", "''")
    text = text.replace("\\n", "\n").replace("\\t", "\t")

    return text


def parse_sql_from_code_block(text: str) -> str:
    """
    Returns cleaned SQL query string compatible with SQLite,
    by removing markdown fences and fixing escaping.
    """
    return trim_code_block(text, "sql")
