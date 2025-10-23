import json, os
from PyQt6.QtCore import QObject, pyqtSignal

class SettingsManager(QObject):
    settings_changed = pyqtSignal(str, object)

    def __init__(self):
        super().__init__()
        self.setting_file = 'clipmate_settings.json'
        self.settings = self.load_settings()

    def load_settings(self):
        default_settings = {
            'max_history_size': 10,
            'start_minimized': False,
            'auto_clear_interval': 0,
            'hotkey_paste': 'Ctrl+Shift+V'
        }

        if os.path.exists(self.setting_file):
            try:
                with open(self.setting_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    default_settings.update(loaded_settings)
            except Exception:
                pass

        return default_settings

    def save_settings(self):
        try:
            with open(self.setting_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get_settings(self, key, default = None):
        return self.settings.get(key, default)

    def set_settings(self, key, value):
        if self.settings.get(key) != value:
            self.settings[key] = value
            self.settings_changed.emit(key, value)
            self.save_settings()
