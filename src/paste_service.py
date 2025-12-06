import keyboard
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QObject, QTimer

class PasteService(QObject):
    def __init__(self):
        super().__init__()

    def paste_text(self, text):
        if not text or text.strip() == '':
            return

        self._minimize_windows()
        QTimer.singleShot(100, lambda: self._do_paste_text(text))

    def paste_image(self, pixmap):
        if pixmap.isNull():
            return

        self._minimize_windows()
        QTimer.singleShot(100, lambda: self._do_paste_image(pixmap))

    def _do_paste_text(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        keyboard.send('ctrl+v')
        self._show_windows()

    def _do_paste_image(self, pixmap):
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(pixmap)
        keyboard.send('ctrl+v')
        self._show_windows()

    def _minimize_windows(self):
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QMainWindow) and widget.windowTitle() == 'ClipMate':
                widget.showMinimized()

    def _show_windows(self):
        QTimer.singleShot(50, lambda: self._restore_windows())

    def _restore_windows(self):
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QMainWindow) and widget.windowTitle() == 'ClipMate':
                widget.showNormal()
                widget.raise_()
                widget.activateWindow()
                break