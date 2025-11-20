import sys
from PyQt6.QtWidgets import QApplication
from src.tray_manager import TrayManager
from src.clipboard_manager import ClipboardManager
from src.settings_manager import SettingsManager
from src.main_window import MainUI
from src.settings_window import SettingsUI

class ClipMateApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.settings = SettingsManager()
        self.clipboard = ClipboardManager(self.settings)
        self.main_ui = MainUI(self.settings, self.clipboard)
        self.settings_ui = SettingsUI(self.settings)
        self.tray = TrayManager(self.settings)

        self.connect_signals()

    def connect_signals(self):
        self.clipboard.history_updated.connect(self.main_ui.update_history_list)
        self.clipboard.pinned_history_updated.connect(self.main_ui.update_pinned_history)

        self.main_ui.paste_requested.connect(self.clipboard.paste_to_active_app)
        self.main_ui.clear_history_requested.connect(
            lambda: self.clipboard.update_and_save_history([])
        )
        self.main_ui.clear_pinned_history_requested.connect(
            lambda: self.clipboard.update_and_save_pinned_history([])
        )
        self.main_ui.filter_text_changed.connect(self.clipboard.on_filter_text_changed)
        self.main_ui.pin_current_requested.connect(self.main_ui.pin_selected_item)
        self.main_ui.remove_from_pinned_requested.connect(self.clipboard.remove_from_pinned)

        self.tray.show_main.connect(self.show_main_window)
        self.tray.show_settings.connect(self.settings_ui.show)
        self.tray.quit_app.connect(self.quit_app)

        self.main_ui.show_settings.connect(self.settings_ui.show)

    def show_main_window(self):
        self.main_ui.show()
        self.main_ui.raise_()
        self.main_ui.activateWindow()

    def quit_app(self):
        self.tray.cleanup()
        self.app.quit()

    def run(self):
        self.main_ui.show()
        return self.app.exec()


if __name__ == '__main__':
    app = ClipMateApp()
    sys.exit(app.run())