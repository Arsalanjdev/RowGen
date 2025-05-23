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


# print(
#     parse_sql_from_code_block(
#         """```sql
# INSERT INTO users (id, name, username, rank) VALUES
# (1, 'Alice Johnson', 'alicej', 3),
# (2, 'Bob Smith', 'bobsmith', 1),
# (3, 'Charlie Brown', 'charlieb', 2),
# (4, 'Diana Prince', 'dianap', 4),
# (5, 'Evan Wright', 'evanw', 5),
# (6, 'Fiona Gallagher', 'fionag', 2),
# (7, 'George King', 'georgek', 3),
# (8, 'Hannah Montana', 'hannahm', 1),
# (9, 'Ian McKellen', 'ianm', 4),
# (10, 'Jessica Jones', 'jessicaj', 5),
# (11, 'Kevin Hart', 'kevinh', 2),
# (12, 'Laura Palmer', 'laurap', 3),
# (13, 'Michael Scott', 'michaels', 1),
# (14, 'Nancy Drew', 'nancyd', 4),
# (15, 'Oscar Wilde', 'oscarw', 5),
# (16, 'Pam Beesly', 'pamb', 2),
# (17, 'Quincy Jones', 'quincyj', 3),
# (18, 'Rachel Green', 'rachelg', 1),
# (19, 'Steve Rogers', 'stever', 4),
# (20, 'Tina Fey', 'tinaf', 5);
# ```"""
#     )
# )
