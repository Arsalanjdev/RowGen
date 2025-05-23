import os
import tempfile

import pytest
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    create_engine,
    MetaData,
    Table,
)

from rowgen.extract_from_db import (
    extract_db_schema,
)


@pytest.fixture(scope="function")
def sqlite_db_url():
    return "sqlite:///:memory:"


@pytest.fixture(scope="function")
def setup_database():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_url = f"sqlite:///{tmp.name}"
    engine = create_engine(db_url)
    metadata = MetaData()

    parent = Table(
        "parent",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String, nullable=False, unique=True),
        CheckConstraint("length(name) > 1", name="name_length_check"),
    )

    child = Table(
        "child",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("parent_id", Integer, ForeignKey("parent.id", ondelete="CASCADE")),
        UniqueConstraint("parent_id", name="uq_child_parent_id"),
    )

    metadata.create_all(engine)
    yield db_url  # yield the URL instead of the engine
    engine.dispose()
    os.remove(tmp.name)


def test_extract_schema_basic(setup_database):
    db_url = setup_database
    schema = extract_db_schema(db_url)
    assert "tables" in schema
    assert "parent" in schema["tables"]
    assert "child" in schema["tables"]

    parent = schema["tables"]["parent"]
    assert any(c["primary_key"] for c in parent["columns"])
    assert any(c["unique"] or c["name"] == "name" for c in parent["columns"])
    assert len(parent["check_constraints"]) > 0
    assert parent["primary_key"] == ["id"]

    child = schema["tables"]["child"]
    assert any(fk["target_table"] == "parent" for fk in child["foreign_keys"])
    assert child["primary_key"] == ["id"]
    assert any(uc["name"] == "uq_child_parent_id" for uc in child["unique_constraints"])


def test_invalid_url_raises():
    with pytest.raises(Exception, match="Failed to extract schema"):
        extract_db_schema("invalid_url")
