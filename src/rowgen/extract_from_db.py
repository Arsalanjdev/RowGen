"""
Extracts information (schema) from a SQL database.
"""

from typing import Dict, List

from sqlalchemy import create_engine, inspect


class DBconnect:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.inspector = inspect(self.engine)

    @property
    def tables(self) -> List[str]:
        return self.inspector.get_table_names()

    @property
    def table_columns(self) -> Dict[str, List[Dict]]:
        return {table: self.inspector.get_columns(table) for table in self.tables}
