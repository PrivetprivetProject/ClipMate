import json
import os
import sys
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

class SettingsManager(QObject):
    settings_changed = pyqtSignal(str, object)

    def __init__(self):
        super().__init__()
        self.setting_path = self.get_settings_path()
        self.settings = self.load_settings()

    def get_settings_path(self):
        if getattr(sys, 'frozen', False):
            base_path = Path.home() / 'AppData' / 'Roaming' / 'ClipMate'
        else:
            base_path = Path(__file__).parent.parent / 'data'

        base_path.mkdir(parents=True, exist_ok=True)

        return base_path / 'clipmate_settings.json'

    def load_settings(self):
        default_settings = {
            'history': [],
            'pinned_history': [],
            'images': [],
            'global_hotkey': 'Ctrl+Shift+H',
            'tabs_data': {},
            'tabs_order': ['Главная', 'Изображения', 'Избранное'],
            'current_theme': 'light'
        }

        if os.path.exists(self.setting_path):
            try:
                with open(self.setting_path, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    default_settings.update(loaded_settings)
            except Exception:
                pass

        return default_settings

    def save_settings(self):
        try:
            with open(self.setting_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        if self.settings.get(key) != value:
            self.settings[key] = value
            self.settings_changed.emit(key, value)
            self.save_settings()