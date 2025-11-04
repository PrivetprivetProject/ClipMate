import keyboard
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow

class ClipboardManager(QObject):
    history_updated = pyqtSignal(list)

    def __init__(self, settings_manager):
        super().__init__()
        self.settings = settings_manager
        self.clipboard = QApplication.clipboard()
        self.full_history = settings_manager.get_history()
        self.filtered_history = self.full_history.copy()
        self.max_size = settings_manager.get('max_history_size')
        self.current_filter = ''

        self.clipboard.dataChanged.connect(self.on_clipboard_change)
        settings_manager.settings_changed.connect(self.on_settings_change)

    def on_settings_change(self, key, value):
        if key == 'max_history_size':
            self.max_size = value
            if len(self.full_history) > self.max_size:
                self.update_and_save_history(self.full_history[:self.max_size])

    def on_clipboard_change(self):
        text = self.clipboard.text().strip()
        if text and text not in self.full_history:
            new_history = [text] + self.full_history
            if len(new_history) > self.max_size:
                new_history = new_history[:self.max_size]

            self.update_and_save_history(new_history)

    def update_and_save_history(self, history):
        self.full_history = history
        self.filtered_history = history[:]
        self.current_filter = ''
        self.history_updated.emit(history)
        self.settings.save_history(history)

    def paste_to_active_app(self, text):
        self.minimize_windows()
        QTimer.singleShot(100, lambda: self.do_paste(text))

    def do_paste(self, text):
        self.clipboard.setText(text)
        keyboard.send('ctrl+v')

    def minimize_windows(self):
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QMainWindow):
                widget.showMinimized()

    def on_filter_text_changed(self, filter_text):
        self.current_filter = filter_text.lower().strip()
        self.filtered_history = self.full_history if not self.current_filter else [
                text for text in self.full_history
                if self.current_filter in text.lower()
            ]

        self.history_updated.emit(self.filtered_history)
