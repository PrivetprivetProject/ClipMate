from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QHBoxLayout,
                             QPushButton, QLabel)
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
import base64

class ImageTabWidget(QWidget):
    paste_requested = pyqtSignal(str)
    remove_requested = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.images = []
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.images_list = QListWidget()
        self.images_list.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.images_list.setIconSize(QSize(100, 100))
        self.images_list.setSpacing(5)
        layout.addWidget(self.images_list)

        button_layout = QHBoxLayout()

        self.paste_btn = QPushButton('Вставить выбранное')
        self.paste_btn.clicked.connect(self._on_paste_clicked)
        button_layout.addWidget(self.paste_btn)

        self.remove_btn = QPushButton('Удалить выбранное')
        self.remove_btn.clicked.connect(self._on_remove_clicked)
        button_layout.addWidget(self.remove_btn)

        layout.addLayout(button_layout)

    def _on_item_double_clicked(self, item):
        if hasattr(item, 'image_data'):
            self.paste_requested.emit(item.image_data)

    def _on_paste_clicked(self):
        selected_image = self.get_selected_image()
        if selected_image:
            self.paste_requested.emit(selected_image)

    def _on_remove_clicked(self):
        selected_image = self.get_selected_image()
        if selected_image:
            self.remove_requested.emit(selected_image)

    def update_images(self, images_base64):
        self.images = images_base64
        self.images_list.clear()

        for i, image_base64 in enumerate(images_base64, 1):
            item = QListWidgetItem(f'Изображение {i}')
            item.image_data = image_base64

            pixmap = self._base64_to_pixmap(image_base64)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(100, 100,
                                              Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                item.setIcon(QIcon(scaled_pixmap))

                size_info = f"Размер: {pixmap.width()}x{pixmap.height()}"
                item.setToolTip(f"{size_info}\nДвойной клик для вставки")

                item.setText(f'Изображение {i} ({pixmap.width()}x{pixmap.height()})')
            else:
                item.setToolTip('Не удалось загрузить изображение')

            self.images_list.addItem(item)

    def _base64_to_pixmap(self, base64_str):
        try:
            if ',' in base64_str:
                base64_str = base64_str.split(',')[1]

            image_data = base64.b64decode(base64_str)
            pixmap = QPixmap()
            success = pixmap.loadFromData(image_data)
            if not success:
                return QPixmap()
            return pixmap
        except Exception:
            return QPixmap

    def get_selected_image(self):
        selected_items = self.images_list.selectedItems()
        if selected_items:
            return selected_items[0].image_data
        return None

    def clear_images(self):
        self.images = []
        self.images_list.clear()