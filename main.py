import sys
from PyQt6.QtWidgets import (QApplication)
from PyQt6.QtCore import (Qt)
from tray_manager import TrayManager
from clipboard_manager import ClipboardManager
from settings_manager import SettingsManager
from ui_components import MainUI

class ClipMateApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.main_ui = MainUI()
        self.clipboard_manager = ClipboardManager(self.main_ui)
        self.settings_manager = SettingsManager()
        self.tray_manager = TrayManager(
            main_ui=self.main_ui,
            clipboard_manager=self.clipboard_manager,
            settings_manager=self.settings_manager
        )

        self.setup_connection()

    def setup_connection(self):
        self.clipboard_manager.history_updated.connect(self.main_ui.update_history_list)
        self.main_ui.paste_requested.connect(self.clipboard_manager.paste_to_active_app)
        self.settings_manager.settings_changed.connect(self.on_settings_changed)

        self.tray_manager.show_main_requested.connect(self.main_ui.show_main_window)
        self.tray_manager.show_settings_requested.connect(self.main_ui.show_settings_window)
        self.tray_manager.hide_requested.connect(self.main_ui.hide)
        self.tray_manager.quit_requested.connect(self.app.quit)

    def on_settings_changed(self, key, value):
        if key == 'max_history_size':
            self.clipboard_manager.set_max_history_size(value)

    def run(self):
        self.main_ui.show()
        return self.app.exec()

if __name__ == '__main__':
    app = ClipMateApp()
    sys.exit(app.run())