import json, os, pytest
from src.settings_manager import SettingsManager

TEST_FILE = 'test_clipmate_settings.json'

@pytest.fixture(autouse=True)
def remove_test_file():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_default_settings(tmp_path, monkeypatch):
    monkeypatch.setattr(SettingsManager, 'settings_file', str(tmp_path/TEST_FILE))

    sm = SettingsManager()
    sm.set('max_history_size', 20)
    sm.save_history(['a', 'b'])
    sm.save_pinned_history(['x'])

    sm2 = SettingsManager()
    assert sm2.get('max_history_size') == 20
    assert sm2.get_history() == ['a', 'b']
    assert sm2.get_pinned_history() == ['x']

def test_settings_changed_signal(qapp, monkeypatch):
    changes = []

    def capture(key, val):
        changes.append((key, val))

    sm = SettingsManager()
    sm.settings_changed.connect(capture)

    sm.set('max_history_size', 30)
    assert changes == [('max_history_size', 30)]