import pytest

from settings_manager import SettingsManager
from tray_manager import TrayManager


def test_hotkey_update(monkeypatch):
    added = []

    def add(seq, func):
        added.append((seq, func))
        return 'hotkey-id'

    monkeypatch.setattr('keyboard.add_hotkey', add)
    monkeypatch.setattr('keyboard.remove_hotkey', lambda id: None)

    sm = SettingsManager()
    tm = TrayManager(sm)

    assert added[0][0] == 'Ctrl+Shift+H'

    sm.set('global_hotkey', 'alt+f4')
    assert added[1][0] == 'alt+f4'