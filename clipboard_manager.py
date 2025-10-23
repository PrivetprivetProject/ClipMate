import pyautogui
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtGui import QClipboard
from PyQt6.QtWidgets import QApplication

class ClipboardManager(QObject):
    history_updated = pyqtSignal(list)

    def __init__(self, main_ui):
        super().__init__()
        self.main_ui = main_ui
        self.clipboard = QApplication.clipboard()
        self.clipboard_history = []
        self.max_history_size = 10

        self.setup_clipboard_monitoring()

    def setup_clipboard_monitoring(self):
        self.clipboard.dataChanged.connect(self.on_clipboard_changed)

    def on_clipboard_changed(self):
        current_text = self.clipboard.text().strip()
        if current_text not in self.clipboard_history:
            self.clipboard_history.insert(0, current_text)
            if len(self.clipboard_history) > self.max_history_size:
                self.clipboard_history = self.clipboard_history[:self.max_history_size]

            self.history_updated.emit(self.clipboard_history)

    def paste_to_active_app(self, text):
        self.main_ui.showMinimized()
        QTimer.singleShot(300, lambda: self._perform_paste(text))

    def _perform_paste(self, text):
        self.clipboard.setText(text)
        pyautogui.hotkey('ctrl', 'v')

        QTimer.singleShot(100, self._restore_main_ui)

    def _restore_main_ui(self):
        self.main_ui.showNormal()
        self.main_ui.activateWindow()


    def clear_history(self):
        self.clipboard_history.clear()
        self.history_updated.emit(self.clipboard_history)

    def set_max_history_size(self, size):
        self.max_history_size = size
        if len(self.clipboard_history) > size:
            self.clipboard_history = self.clipboard_history[:size]
            self.history_updated.emit(self.clipboard_history)

    def get_history(self):
        return self.clipboard_history.copy()