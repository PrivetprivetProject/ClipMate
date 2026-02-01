from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QBuffer, QByteArray, QIODevice, QObject, pyqtSignal
from src.history_service import HistoryService
from src.paste_service import PasteService

class ClipboardManager(QObject):
    history_updated = pyqtSignal(list)
    pinned_history_updated = pyqtSignal(list)
    images_updated = pyqtSignal(list)

    def __init__(self, settings_manager):
        super().__init__()
        self.settings = settings_manager
        self.clipboard = QApplication.clipboard()

        self.history_service = HistoryService(settings_manager)
        self.paste_service = PasteService()

        self.history_service.history_updated.connect(self.history_updated)
        self.history_service.pinned_history_updated.connect(self.pinned_history_updated)
        self.history_service.images_updated.connect(self.images_updated)

        self._block_clipboard_change = False
        self.clipboard.dataChanged.connect(self.on_clipboard_change)

        settings_manager.settings_changed.connect(self.on_settings_change)

        self.last_text = ''
        self.last_image_hash = ''

    def on_clipboard_change(self):
        if self._block_clipboard_change:
            return

        try:
            self._block_clipboard_change = True

            pixmap = self.clipboard.pixmap()
            if not pixmap.isNull():
                current_image_hash = self.get_image_hash(pixmap)

                if current_image_hash != self.last_image_hash:
                    self.last_image_hash = current_image_hash
                    self.last_text = ''
                    self.history_service.add_image(pixmap)
                    return
                else:
                    return

            text = self.clipboard.text().strip()
            if text:
                if text != self.last_text:
                    self.last_text = text
                    self.last_image_hash = ''
                    self.history_service.add_to_history(text)
                else:
                    return

        except Exception:
            pass
        finally:
            self._block_clipboard_change = False

    def get_image_hash(self, pixmap):
        try:
            image = pixmap.toImage()
            if image.isNull():
                return 'null_image'

            size = f'{image.width()}x{image.height()}'

            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.OpenModeFlag.WriteOnly)

            success = pixmap.save(buffer, "PNG")
            if not success:
                return f'{size}_save_failed'

            buffer.close()

            data = byte_array.data()
            sample_size = min(1000, len(data))
            sample_data = data[:sample_size] if data else b''

            return f'{size}_{hash(sample_data) % 100000}'

        except Exception:
            return 'error_hash'

    def on_settings_change(self, key, value):
        if key == 'max_history_size':
            self.history_service.update_max_size(value)
        elif key == 'max_images_size':
            self.history_service.update_max_images_size(value)

    def pin_current_item(self):
        self.history_service.pin_current_item()

    def pin_selected_text(self, text):
        self.history_service.pin_text(text)

    def remove_from_pinned(self, text):
        self.history_service.remove_pinned(text)

    def paste_to_active_app(self, text):
        self.paste_service.paste_text(text)

    def on_filter_text_changed(self, filter_text):
        self.history_service.filter_items(filter_text)

    def paste_image_to_active_app(self, image_base64):
        pixmap = self.history_service.get_image_pixmap(image_base64)
        if not pixmap.isNull():
            self.paste_service.paste_image(pixmap)

    def remove_image(self, image_base64):
        self.history_service.remove_image(image_base64)

    def clear_images(self):
        self.history_service.clear_images()