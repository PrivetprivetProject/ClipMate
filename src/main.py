import sys
from PyQt6.QtWidgets import QApplication
from src.tray_manager import TrayManager
from src.clipboard_manager import ClipboardManager
from src.settings_manager import SettingsManager
from src.main_window import MainUI
from src.settings_window import SettingsUI
from src.styles import get_theme_styles

class ClipMateApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.settings = SettingsManager()

        saved_theme = self.settings.get('current_theme', 'light')
        self.apply_styles(saved_theme)

        self.clipboard = ClipboardManager(self.settings)
        self.main_ui = MainUI(self.settings, self.clipboard)
        self.settings_ui = SettingsUI(self.settings)
        self.tray = TrayManager(self.settings)

        self.connect_signals()

    def apply_styles(self, theme_name='light'):
        styles = get_theme_styles(theme_name)
        self.app.setStyleSheet('')
        QApplication.processEvents()
        self.app.setStyleSheet(styles)
        if hasattr(self, 'main_ui'):
            self.main_ui.update_menu_style(theme_name)

    def on_settings_changed(self, key, value):
        if key == 'current_theme':
            self.apply_styles(value)
            if self.main_ui.isVisible():
                self.main_ui.resize(self.main_ui.size().width(), self.main_ui.size().height())
            if self.settings_ui.isVisible():
                self.settings_ui.resize(
                    self.settings_ui.size().width(), self.settings_ui.size().height()
                )

    def connect_signals(self):
        self.clipboard.history_updated.connect(self.main_ui.update_history_list)
        self.clipboard.pinned_history_updated.connect(self.main_ui.update_pinned_history)
        self.clipboard.images_updated.connect(self.main_ui.update_images_list)

        self.main_ui.paste_requested.connect(self.clipboard.paste_to_active_app)
        self.main_ui.paste_image_requested.connect(self.clipboard.paste_image_to_active_app)

        self.main_ui.clear_history_requested.connect(
            lambda: self.clipboard.history_service.clear_history()
        )
        self.main_ui.clear_pinned_history_requested.connect(
            lambda: self.clipboard.history_service.clear_pinned_history()
        )
        self.main_ui.clear_images_requested.connect(
            lambda: self.clipboard.clear_images()
        )
        self.main_ui.filter_text_changed.connect(self.clipboard.on_filter_text_changed)
        self.main_ui.pin_current_requested.connect(self.main_ui.pin_selected_item)
        self.main_ui.remove_from_pinned_requested.connect(self.clipboard.remove_from_pinned)
        self.main_ui.remove_image_requested.connect(self.clipboard.remove_image)
        self.main_ui.quit_requested.connect(self.quit_app)

        self.tray.show_main.connect(self.show_main_window)
        self.tray.show_settings.connect(self.settings_ui.show)
        self.tray.quit_app.connect(self.quit_app)

        self.main_ui.show_settings.connect(self.settings_ui.show)
        self.settings.settings_changed.connect(self.on_settings_changed)

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