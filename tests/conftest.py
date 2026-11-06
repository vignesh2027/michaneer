import pytest


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setenv("MICHANEER_DB", str(tmp_path / "test.db"))
    yield tmp_path / "test.db"
