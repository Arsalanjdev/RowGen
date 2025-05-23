from rowgen.sql_parser import parse_sql_from_code_block


def test_parsing_one_sql_statement():
    sql_statement = """```sql
    INSERT INTO users (id, name, username, rank) VALUES
    (1, 'Alice Johnson', 'alicej', 3),
    (2, 'Bob Smith', 'bobsmith', 1)"""
    sql_result = """INSERT INTO users (id, name, username, rank) VALUES
    (1, 'Alice Johnson', 'alicej', 3),
    (2, 'Bob Smith', 'bobsmith', 1)"""
    assert parse_sql_from_code_block(sql_statement) == sql_result
