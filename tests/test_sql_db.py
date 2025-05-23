import os
import sqlite3

import pytest
from sqlalchemy import INTEGER, TEXT
from sqlalchemy.exc import OperationalError

from rowgen.extract_from_db import DBconnect


@pytest.fixture
def temp_db():
    db_path = "test.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    username TEXT UNIQUE,
    rank INTEGER);
    """
    )
    conn.commit()
    conn.close()
    url = f"sqlite:///{db_path}"
    yield url
    # Cleanup after test
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def db_connect(temp_db):
    dbc = DBconnect(temp_db)
    yield dbc


@pytest.fixture
def empty_temp_db():
    db_path = "empty_test.db"
    conn = sqlite3.connect(db_path)
    conn.close()
    url = f"sqlite:///{db_path}"
    yield url
    if os.path.exists(db_path):
        os.remove(db_path)


def test_empty_db_table_columns(empty_temp_db):
    dbc = DBconnect(empty_temp_db)
    assert dbc.table_columns == {}


def test_get_columns(db_connect):
    # cols = db_connect.table_columns
    expected = {
        "users": [
            {
                "name": "id",
                "type": INTEGER(),
                "nullable": True,
                "default": None,
                "primary_key": 1,
            },
            {
                "name": "name",
                "type": TEXT(),
                "nullable": False,
                "default": None,
                "primary_key": 0,
            },
            {
                "name": "username",
                "type": TEXT(),
                "nullable": True,
                "default": None,
                "primary_key": 0,
            },
            {
                "name": "rank",
                "type": INTEGER(),
                "nullable": True,
                "default": None,
                "primary_key": 0,
            },
        ]
    }

    result = db_connect.table_columns

    # We compare only the relevant parts because type() instances won't compare cleanly
    def clean(col):
        return {
            "name": col["name"],
            "type": type(col["type"]),  # type comparison by class
            "nullable": col["nullable"],
            "default": col["default"],
            "primary_key": col["primary_key"],
        }

    cleaned_result = {
        table: [clean(col) for col in cols] for table, cols in result.items()
    }

    cleaned_expected = {
        table: [clean(col) for col in cols] for table, cols in expected.items()
    }

    assert cleaned_result == cleaned_expected


def test_invalid_db_url():
    bad_url = "sqlite:///non_existent_folder/non_existent_file.db"
    with pytest.raises(OperationalError):
        DBconnect(bad_url)


def test_tables_list(db_connect):
    tables = db_connect.tables
    assert "users" in tables
