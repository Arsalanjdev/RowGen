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
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Executes insert statements into the database directly.",
    )

    args = parser.parse_args()

    if args.db_url:
        db_url = args.db_url
    else:
        db_url = "{args.db_type}://{args.user}:{args.password}@{args.host}:{args.port}/{args.database}"

    dbc = DBconnect(db_url)
    hf = HFapi()
    ai_sql_response = hf.prompt_fake_data(dbc.table_columns, 20)
    sql_statements = parse_sql_from_code_block(ai_sql_response)
    # execute
    if args.execute:
        sql_statements = sql_statements.split("\n")
        engine = create_engine(
            "sqlite:///testrowgendb.sqlite"
        )  # replace with your DB URL
        with engine.connect() as connection:
            for sql in sql_statements:
                connection.execute(text(sql))
            connection.commit()
        print("Insert statements were executed into the database.")
    else:
        with open("init_db.sql", "w") as f:
            f.write(sql_statements)
        print("Saved to sql file.")


if __name__ == "__main__":
    main()
