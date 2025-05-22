from sqlalchemy import create_engine, text

from hf_api import HFapi
import argparse

from rowgen.extract_from_db import DBconnect
from rowgen.parser import parse_sql_from_code_block


def main():
    parser = argparse.ArgumentParser(description="RowGen CLI")
    parser.add_argument(
        "--db-url", help="Full database URL (overrides individual parts)"
    )
    parser.add_argument(
        "--db-type", choices=["postgresql", "mysql", "sqlite"], default="postgresql"
    )
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default="5432")
    parser.add_argument("--user")
    parser.add_argument("--password")
    parser.add_argument("--database")

    args = parser.parse_args()

    if args.db_url:
        db_url = args.db_url
    else:
        db_url = "{args.db_type}://{args.user}:{args.password}@{args.host}:{args.port}/{args.database}"

    dbc = DBconnect(db_url)
    hf = HFapi()
    data = hf.prompt_fake_data(dbc.table_columns, 20)
    inserts = hf.prompt_insert_statements(data, table_name="users")
    # print(inserts)
    sql_parser = parse_sql_from_code_block(inserts)
    sql_parser = sql_parser.split("\n")
    print(sql_parser)
    # execute
    engine = create_engine("sqlite:///testrowgendb.sqlite")  # replace with your DB URL
    with engine.connect() as connection:
        for sql in sql_parser:
            connection.execute(text(sql))
        connection.commit()


if __name__ == "__main__":
    main()
