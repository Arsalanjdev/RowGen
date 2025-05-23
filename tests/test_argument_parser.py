import sys

import pytest

from rowgen.main import get_parser


def test_db_url_and_apikey(monkeypatch):
    test_args = ["prog", "--db-url", "sqlite:///test.db", "--apikey", "ABC123"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = get_parser().parse_args()
    assert args.db_url == "sqlite:///test.db"
    assert args.apikey == "ABC123"
    assert not args.execute


def test_execute_flag(monkeypatch):
    test_args = ["prog", "--execute"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = get_parser().parse_args()
    assert args.execute is True


def test_default_values(monkeypatch):
    test_args = ["prog"]
    monkeypatch.setattr(sys, "argv", test_args)
    args = get_parser().parse_args()
    assert args.db_type == "postgresql"
    assert args.host == "localhost"
    assert args.port == "5432"
    assert args.apikey is None


def test_invalid_db_type(monkeypatch):
    test_args = ["prog", "--db-type", "oracle"]
    monkeypatch.setattr(sys, "argv", test_args)
    with pytest.raises(SystemExit):  # argparse exits on bad input
        get_parser().parse_args()
