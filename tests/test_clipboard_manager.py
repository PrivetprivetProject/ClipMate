import pytest
from src.clipboard_manager import ClipboardManager
from PyQt6.QtCore import QMimeData

from src.settings_manager import SettingsManager


@pytest.fixture
def fake_clipboard(monkeypatch):
    class FakeClipboard:
        def __init__(self):
            self._text = ''
            self.dataChanged = type('Signal', (), {'connect': lambda *a:None})()

        def text(self): return self._text
        def setText(self, txt): self._text = txt

    fake = FakeClipboard()
    monkeypatch.setattr('PyQt6.QtWidgets.QApplication.clipboard', lambda: fake)
    return fake

@pytest.fixture
def mock_keyboard(monkeypatch):
    calls = []
    def send(keys):
        calls.append(keys)

    monkeypatch.setattr('keyboard.send', send)
    return calls

def test_clipboard_change(qapp, fake_clipboard, mock_keyboard):
    sm = SettingsManager()
    cbm = ClipboardManager(sm)

    fake_clipboard.setText('Hello')
    cbm.on_clipboard_change()

    assert sm.get_history() == ['Hello']

def test_paste_to_active_app(qapp, fake_clipboard, mock_keyboard):
    sm = SettingsManager()
    cbm = ClipboardManager(sm)

    cbm.paste_to_active_app('World')
    assert fake_clipboard.text() == 'World'
    assert mock_keyboard[0] == 'ctrl+v'

def test_filter_text_changed(qapp, fake_clipboard):
    sm = SettingsManager()
    cbm = ClipboardManager(sm)

    sm.save_history(['apple', 'banana', 'cherry'])
    cbm.on_filter_text_changed('an')
    assert cbm.filtered_history == ['banana']

def test_pin_selected_text(qapp, fake_clipboard):
    sm = SettingsManager()
    cbm = ClipboardManager(sm)

    sm.save_pinned_history([])
    cbm.pin_selected_text('apple')
    assert sm.get_pinned_history() == ['apple']