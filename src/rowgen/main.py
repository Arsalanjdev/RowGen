import argparse
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from rowgen.extract_from_db import extract_db_schema
from rowgen.hf_api import HFapi
from rowgen.sql_parser import parse_sql_from_code_block


def get_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="RowGen CLI - Generate and insert synthetic data into databases"
    )

    # Database connection options
    db_group = parser.add_argument_group("Database Connection")
    db_group.add_argument(
        "--db-url",
        help="Full database URL (overrides individual connection parameters)",
    )
    db_group.add_argument(
        "--db-type",
        choices=["postgresql", "mysql", "sqlite"],
        default="postgresql",
        help="Database type (default: postgresql)",
    )
    db_group.add_argument("--host", default="localhost", help="Database host")
    db_group.add_argument("--port", default="5432", help="Database port")
    db_group.add_argument("--user", help="Database username")
    db_group.add_argument("--password", help="Database password")
    db_group.add_argument("--database", help="Database name")

    # Operation options
    operation_group = parser.add_argument_group("Operation")
    operation_group.add_argument(
        "--execute",
        action="store_true",
        help="Execute insert statements directly in the database",
    )
    operation_group.add_argument(
        "--rows",
        type=int,
        default=25,
        help="Number of rows to generate (default: 25)",
    )
    operation_group.add_argument(
        "--output",
        default="inserts.sql",
        help="Output file path when not executing directly (default: inserts.sql)",
    )

    # API configuration
    api_group = parser.add_argument_group("API Configuration")
    api_group.add_argument(
        "--apikey",
        help="HuggingFace Hub API key (will be saved in config if not present)",
    )

    return parser


def validate_args(args: argparse.Namespace) -> bool:
    """Validate that required arguments are provided."""
    if not args.db_url and not all([args.host, args.user, args.database]):
        print("Error: Either provide --db-url or all of --host, --user, --database")
        return False
    return True


def get_db_url(args: argparse.Namespace) -> str:
    """Construct the database URL from arguments."""
    if args.db_url:
        return args.db_url

    credentials = f"{args.user}:{args.password}" if args.password else args.user
    return f"{args.db_type}://{credentials}@{args.host}:{args.port}/{args.database}"


def execute_sql_statements(db_url: str, sql_statements: str) -> None:
    """Execute SQL statements against the database."""
    try:
        engine = create_engine(db_url)
        with engine.connect() as connection:
            # Split and filter empty statements
            statements = [stmt for stmt in sql_statements.split(";") if stmt.strip()]

            for sql in statements:
                if sql.strip():  # Skip empty statements
                    connection.execute(text(sql.strip()))
            connection.commit()
        print("Successfully executed insert statements.")
    except SQLAlchemyError as e:
        print(f"Error executing SQL statements: {e}")
        raise


def save_sql_statements(output_path: str, sql_statements: str) -> None:
    """Save SQL statements to a file."""
    try:
        with open(output_path, "w") as f:
            f.write(sql_statements)
        print(f"SQL statements saved to {output_path}")
    except IOError as e:
        print(f"Error saving to file: {e}")
        raise


def get_api_key_from_config() -> str:
    """
    Retrieves API key from the config file (~/.config/rowgen/conf).
    If no key is stored, prompts the user for input and saves it.

    :return: The API key as a string
    :raises: SystemExit if there are critical errors
    """
    config_dir = Path.home() / ".config" / "rowgen"
    config_path = config_dir / "conf"

    # Try to read existing API key
    if config_path.exists():
        try:
            with open(config_path, "r") as file:
                for line in file:
                    if line.startswith("apikey:"):
                        return line.split(":", 1)[1].strip()
        except PermissionError:
            print("Error: No permission to read the config file.")
            raise SystemExit(1) from None
        except Exception as e:
            print(f"Error reading config: {e}")
            raise SystemExit(1) from None

    # Prompt for new API key
    apikey = input("Enter your HuggingFace API key: ").strip()
    if not apikey:
        print("Error: API key cannot be empty")
        raise SystemExit(1)

    # Save the new API key
    try:
        config_dir.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as file:
            file.write(f"apikey: {apikey}\n")
        print(f"API key saved to {config_path}")
    except Exception as e:
        print(f"Warning: Could not save API key: {e}")

    return apikey


def main() -> None:
    """Main entry point for the RowGen CLI."""
    parser = get_parser()
    args = parser.parse_args()

    if not validate_args(args):
        parser.print_help()
        raise SystemExit(1)

    try:
        # Get API key
        api_key = args.apikey if args.apikey else get_api_key_from_config()

        # Get database connection
        db_url = get_db_url(args)

        # Generate SQL statements
        schema = extract_db_schema(db_url)
        print("Schema extracted.")
        hf = HFapi(api_key=api_key)
        print("Connected to the api. Sending the database schema...")
        ai_sql_response = hf.prompt_fake_data(schema, args.rows)
        print("Ai is generating fake data for the database...")
        sql_statements = parse_sql_from_code_block(ai_sql_response)
        print("Generative data returned. processing...")

        # Execute or save
        if args.execute:
            execute_sql_statements(db_url, sql_statements)
        else:
            save_sql_statements(args.output, sql_statements)

    except Exception as e:
        print(f"Error: {e}")
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
