import argparse
import os

from sqlalchemy import create_engine, text

from rowgen.extract_from_db import DBconnect
from rowgen.hf_api import HFapi
from rowgen.sql_parser import parse_sql_from_code_block


def get_parser():
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
    parser.add_argument(
        "--rows",
        default=20,
        help="Enter the number of rows you want to be filled with generative data.",
    )
    parser.add_argument("--apikey", help="Enter your huggingface_hub api key.")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.apikey:
        api_key = args.apikey
    else:
        api_key = get_api_key_from_config()

    if args.db_url:
        db_url = args.db_url
    else:
        db_url = "{args.db_type}://{args.user}:{args.password}@{args.host}:{args.port}/{args.database}"

    rows = args.rows

    dbc = DBconnect(db_url)
    hf = HFapi(api_key=api_key)
    ai_sql_response = hf.prompt_fake_data(dbc.table_columns, rows)
    sql_statements = parse_sql_from_code_block(ai_sql_response)

    # execute
    if args.execute:
        sql_statements = sql_statements.split("\n")
        engine = create_engine("sqlite:///testrowgendb.sqlite")
        with engine.connect() as connection:
            for sql in sql_statements:
                connection.execute(text(sql))
            connection.commit()
        print("Insert statements were executed into the database.")
    else:
        with open("init_db.sql", "w") as f:
            f.write(sql_statements)
        print("Saved to sql file.")


def get_api_key_from_config() -> str:
    """
    Retrieves API key from the config file (~/.config/rowgen/conf).
    If no key is stored, prompts the user for input and saves it.

    :return: str. The API key.
    """
    config_path = os.path.expanduser("~/.config/rowgen/conf")
    apikey = None

    try:
        with open(config_path, "r") as file:
            for line in file:
                if line.startswith("apikey:"):
                    apikey = line.split(":", 1)[1].strip()
                    break  # no need to keep reading

    except FileNotFoundError:
        pass  # we'll prompt the user below
    except PermissionError:
        print("You do not have permission to read the config file.")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred while reading: {e}")
        return ""

    if not apikey:
        # Prompt the user
        apikey = input("Enter your API key: ").strip()

        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, "w") as file:
                file.write(f"apikey: {apikey}\n")
                print(f"API key was store in the {config_path}")
        except Exception as e:
            print(f"Failed to save API key: {e}")

    return apikey


if __name__ == "__main__":
    main()
