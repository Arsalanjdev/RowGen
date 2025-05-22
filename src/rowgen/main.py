from sqlalchemy import create_engine, text

from hf_api import HFapi
import argparse


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

    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Connected to database:", result.scalar())


if __name__ == "__main__":
    main()
