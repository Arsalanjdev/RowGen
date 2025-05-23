"""
Database Schema Extractor.
"""

from typing import Dict

from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError


def extract_db_schema(db_url: str) -> Dict:
    """
    Extract complete database schema including constraints

    Args:
        db_url: Database connection string

    Returns:
        Dictionary containing schema with constraints

    Raises:
        Exception: If connection or inspection fails
    """
    try:
        engine = create_engine(db_url)
        inspector = inspect(engine)

        schema = {"database_type": engine.dialect.name, "tables": {}}

        for table_name in inspector.get_table_names():
            # Get columns with constraints
            columns = []
            for col in inspector.get_columns(table_name):
                columns.append(
                    {
                        "name": col["name"],
                        "type": str(col["type"]),
                        "nullable": col["nullable"],
                        "primary_key": col.get("primary_key", False),
                        "unique": col.get("unique", False),
                        "default": (
                            str(col.get("default")) if col.get("default") else None
                        ),
                        "autoincrement": col.get("autoincrement", False),
                    }
                )

            # Get primary key constraints
            pk_constraint = inspector.get_pk_constraint(table_name)

            # Get foreign key constraints
            foreign_keys = []
            for fk in inspector.get_foreign_keys(table_name):
                foreign_keys.append(
                    {
                        "name": fk.get("name"),
                        "source_columns": fk["constrained_columns"],
                        "target_table": fk["referred_table"],
                        "target_columns": fk["referred_columns"],
                        "ondelete": fk.get("ondelete"),
                        "onupdate": fk.get("onupdate"),
                    }
                )

            # Get unique constraints
            unique_constraints = []
            for uc in inspector.get_unique_constraints(table_name):
                unique_constraints.append(
                    {"name": uc["name"], "columns": uc["column_names"]}
                )

            # Get check constraints (if supported)
            check_constraints = []
            if hasattr(inspector, "get_check_constraints"):
                for cc in inspector.get_check_constraints(table_name):
                    check_constraints.append(
                        {"name": cc["name"], "sqltext": cc["sqltext"]}
                    )

            # Add table to schema
            schema["tables"][table_name] = {
                "columns": columns,
                "primary_key": pk_constraint.get("constrained_columns", []),
                "foreign_keys": foreign_keys,
                "unique_constraints": unique_constraints,
                "check_constraints": check_constraints,
            }

        return schema

    except SQLAlchemyError as e:
        raise Exception(f"Failed to extract schema: {str(e)}") from None
