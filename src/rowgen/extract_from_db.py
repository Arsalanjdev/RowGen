"""
Extracts schema information from a SQL database with comprehensive error handling.
"""

from typing import Dict, List, Any

from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError


class DBError(Exception):
    """Base exception for database-related errors in this module."""

    pass


class NoTablesFoundError(DBError):
    """Raised when no tables are found in the database."""

    pass


class DBconnect:
    def __init__(self, db_url: str):
        """
        Initialize database connection.

        Args:
            db_url: Database connection URL

        Raises:
            DBError: If connection to database fails
        """
        try:
            self.engine = create_engine(db_url)
            self.inspector = inspect(self.engine)
        except SQLAlchemyError as e:
            raise DBError(f"Failed to connect to database: {str(e)}") from e

    @property
    def tables(self) -> List[str]:
        """
        Get list of table names in the database.

        Returns:
            List of table names

        Raises:
            NoTablesFoundError: If no tables exist in the database
            DBError: If table listing fails
        """
        try:
            tables = self.inspector.get_table_names()
            if not tables:
                raise NoTablesFoundError("Database contains no tables")
            return tables
        except SQLAlchemyError as e:
            raise DBError(f"Failed to get table list: {str(e)}") from e

    @property
    def table_columns(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get column information for all tables in the database.

        Returns:
            Dictionary mapping table names to their column information

        Raises:
            NoTablesFoundError: If no tables exist in the database
            DBError: If column information retrieval fails
        """
        try:
            tables = self.tables  # This may raise NoTablesFoundError
            return {table: self._get_columns_with_validation(table) for table in tables}
        except SQLAlchemyError as e:
            raise DBError(f"Failed to get column information: {str(e)}") from e

    def _get_columns_with_validation(self, table: str) -> List[Dict[str, Any]]:
        """
        Get column information for a specific table with validation.

        Args:
            table: Table name to inspect

        Returns:
            List of column information dictionaries

        Raises:
            DBError: If no columns found or inspection fails
        """
        try:
            columns = self.inspector.get_columns(table)
            if not columns:
                raise DBError(f"Table '{table}' contains no columns")
            return columns
        except SQLAlchemyError as e:
            raise DBError(f"Failed to inspect table '{table}': {str(e)}") from e
