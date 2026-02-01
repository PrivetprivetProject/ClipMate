from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLabel, QPushButton, QMenu,
                             QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal


class CustomTitleBar(QWidget):
    minimize_clicked = pyqtSignal()
    maximize_clicked = pyqtSignal()
    close_clicked = pyqtSignal()

    show_settings_clicked = pyqtSignal()
    clear_text_history_clicked = pyqtSignal()
    clear_image_history_clicked = pyqtSignal()
    clear_all_history_clicked = pyqtSignal()
    quit_app_clicked = pyqtSignal()
    about_clicked = pyqtSignal()
    pin_item_clicked = pyqtSignal()
    unpin_item_clicked = pyqtSignal()
    add_tab_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.is_maximized = False

        self.setup_ui()
        self.setup_main_menu()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 5, 5)
        layout.setSpacing(5)

        self.menu_btn = QPushButton('☰')
        self.menu_btn.setFixedSize(30, 30)
        self.menu_btn.setObjectName('menuBtn')
        self.menu_btn.clicked.connect(self.show_main_menu)
        layout.addWidget(self.menu_btn)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout.addWidget(self.title_label)

        self.minimize_btn = QPushButton("−")
        self.maximize_btn = QPushButton("❐")
        self.close_btn = QPushButton("✕")

        self.minimize_btn.setObjectName('minimizeBtn')
        self.maximize_btn.setObjectName('maximizeBtn')
        self.close_btn.setObjectName('closeBtn')

        for btn in [self.minimize_btn, self.maximize_btn, self.close_btn]:
            btn.setFixedSize(30, 30)

        self.minimize_btn.clicked.connect(self.minimize_clicked.emit)
        self.maximize_btn.clicked.connect(self.maximize_clicked.emit)
        self.close_btn.clicked.connect(self.close_clicked.emit)

        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.maximize_btn)
        layout.addWidget(self.close_btn)

    def setup_main_menu(self):
        self.main_menu = QMenu(self)
        self.main_menu.setObjectName('mainMenu')

        self.file_menu = QMenu("Файл", self.main_menu)
        self.setup_file_menu()
        self.main_menu.addMenu(self.file_menu)

        about_action = self.main_menu.addAction("О программе")
        about_action.triggered.connect(self.about_clicked.emit)

        self.tools_menu = QMenu("Инструменты", self.main_menu)
        self.setup_tools_menu()
        self.main_menu.addMenu(self.tools_menu)

        self.main_menu.addSeparator()
        self.main_menu.addAction("Добавить вкладку").triggered.connect(self.add_tab_clicked.emit)

    def setup_file_menu(self):
        settings_action = self.file_menu.addAction("Открыть настройки")
        settings_action.triggered.connect(self.show_settings_clicked.emit)

        self.file_menu.addSeparator()

        clear_text_action = self.file_menu.addAction("Удалить историю текста")
        clear_text_action.triggered.connect(self.clear_text_history_clicked.emit)

        clear_image_action = self.file_menu.addAction("Удалить историю изображений")
        clear_image_action.triggered.connect(self.clear_image_history_clicked.emit)

        clear_all_action = self.file_menu.addAction("Удалить всю историю")
        clear_all_action.triggered.connect(self.clear_all_history_clicked.emit)

        self.file_menu.addSeparator()

        quit_action = self.file_menu.addAction("Выход")
        quit_action.triggered.connect(self.quit_app_clicked.emit)

    def setup_tools_menu(self):
        pin_action = self.tools_menu.addAction("Закрепить выделенное")
        pin_action.triggered.connect(self.pin_item_clicked.emit)

        unpin_action = self.tools_menu.addAction("Открепить выделенное")
        unpin_action.triggered.connect(self.unpin_item_clicked.emit)

        self.tools_menu.addSeparator()

    def show_main_menu(self):
        self.main_menu.exec(
            self.menu_btn.mapToGlobal(
                self.menu_btn.rect().bottomLeft()
            )
        )

    def set_title(self, title):
        self.title_label.setText(title)

    def set_maximized(self, maximized):
        self.is_maximized = maximized
        self.maximize_btn.setText("🗗" if maximized else "❐")

    def set_menu_visible(self, visible):
        self.menu_btn.setVisible(visible)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.maximize_clicked.emit()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (event.globalPosition().toPoint() -
                                  self.parent_window.frameGeometry().topLeft())
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_position'):
            self.parent_window.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()