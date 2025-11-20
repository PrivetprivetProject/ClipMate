import threading, keyboard
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QObject, pyqtSignal, Qt


class TrayManager(QObject):
    show_main = pyqtSignal()
    show_settings = pyqtSignal()
    quit_app = pyqtSignal()

    def __init__(self, settings_manager):
        super().__init__()
        self.settings = settings_manager
        self.setup_tray()
        self.update_hotkey()

        settings_manager.settings_changed.connect(self.on_settings_changed)

    def setup_tray(self):
        self.tray = QSystemTrayIcon()
        self.create_icon()
        self.create_menu()
        self.tray.show()
        self.tray.activated.connect(self.on_tray_activated)

    def create_icon(self):
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.lightGray)
        self.tray.setIcon(QIcon(pixmap))

    def create_menu(self):
        menu = QMenu()
        menu.addAction('Показать', self.show_main.emit)
        menu.addSeparator()
        menu.addAction('Настройки', self.show_settings.emit)
        menu.addSeparator()
        menu.addAction('Выход', self.quit_app.emit)
        self.tray.setContextMenu(menu)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_main.emit()

    def update_hotkey(self):
        def start_listener():
            hotkey_sequence = self.settings.get('global_hotkey', 'ctrl+shift+h')

            if hasattr(self, 'current_hotkey'):
                keyboard.remove_hotkey(self.current_hotkey)

            self.current_hotkey = keyboard.add_hotkey(
                hotkey_sequence,
                lambda: self.show_main.emit()
            )

            keyboard.wait()

        hotkey_thread = threading.Thread(target=start_listener, daemon=True)
        hotkey_thread.start()

    def on_settings_changed(self, key):
        if key == 'global_hotkey':
            self.update_hotkey()

    def cleanup(self):
        if hasattr(self, 'current_hotkey'):
            keyboard.remove_hotkey(self.current_hotkey)