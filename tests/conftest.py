import os, pytest
from PyQt6.QtWidgets import QApplication
from unittest.mock import MagicMock, patch


@pytest.fixture(scope='session')
def qapp():
    app = QApplication.instance()
    if not app:
        app = QApplication([])
    return app

@pytest.fixture
def mock_keyboard(monkeypatch):
    class DummyHotkey:
        pass

    monkeypatch.setattr('keyboard.add_hotkey', lambda seq, func: DummyHotkey)
    monkeypatch.setattr('keyboard.remove_hotkey', lambda hk: None)
    monkeypatch.setattr('keyboard.wait', lambda timeout=None: None)

    return DummyHotkey