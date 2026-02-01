from PyQt6.QtCore import QObject, pyqtSignal
from src.image_service import ImageService

class HistoryService(QObject):
    history_updated = pyqtSignal(list)
    pinned_history_updated = pyqtSignal(list)
    images_updated = pyqtSignal(list)

    def __init__(self, settings_manager):
        super().__init__()
        self.settings = settings_manager

        self.full_history = settings_manager.get('history')
        self.filtered_history = self.full_history.copy()
        self.max_size = settings_manager.get('max_history_size')

        self.full_pinned_history = settings_manager.get('pinned_history')
        self.filtered_pinned_history = self.full_pinned_history.copy()
        self.current_filter = ''

        self.image_service = ImageService(settings_manager)
        self.image_service.images_updated.connect(self.images_updated)

    def add_to_history(self, text):
        if text and text not in self.full_history:
            new_history = [text] + self.full_history
            if len(new_history) > self.max_size:
                new_history = new_history[:self.max_size]
            self._update_history(new_history)

    def pin_current_item(self):
        if self.full_history:
            item_to_pin = self.full_history[0]
            self.pin_text(item_to_pin)

    def pin_text(self, text):
        if text and text not in self.full_pinned_history:
            new_pinned_history = [text] + self.full_pinned_history
            self._update_pinned_history(new_pinned_history)

    def remove_pinned(self, text):
        if text and self.full_pinned_history:
            new_pinned_history = [item for item in self.full_pinned_history if item != text]
            self._update_pinned_history(new_pinned_history)

    def update_max_size(self, new_size):
        self.max_size = new_size
        if len(self.full_history) > self.max_size:
            self._update_history(self.full_history[:self.max_size])

    def filter_items(self, filter_text):
        self.current_filter = filter_text.lower().strip()

        self.filtered_history = self.full_history if not self.current_filter else [
            text for text in self.full_history
            if self.current_filter in text.lower()
        ]

        self.filtered_pinned_history = self.full_pinned_history if not self.current_filter else [
            text for text in self.full_pinned_history
            if self.current_filter in text.lower()
        ]

        self.history_updated.emit(self.filtered_history)
        self.pinned_history_updated.emit(self.filtered_pinned_history)

    def _update_history(self, history):
        self.full_history = history
        self.filtered_history = history[:]
        self.settings.set('history', history)
        self.history_updated.emit(history)

    def _update_pinned_history(self, pinned_history):
        self.full_pinned_history = pinned_history
        self.filtered_pinned_history = pinned_history[:]
        self.settings.set('pinned_history', pinned_history)
        self.pinned_history_updated.emit(pinned_history)

    def clear_history(self):
        self._update_history([])

    def clear_pinned_history(self):
        self._update_pinned_history([])

    def add_image(self, pixmap):
        return self.image_service.add_image(pixmap)

    def remove_image(self, image_base64):
        return self.image_service.remove_image(image_base64)

    def clear_images(self):
        self.image_service.clear_images()

    def update_max_images_size(self, new_size):
        self.image_service.update_max_size(new_size)

    def get_image_pixmap(self, image_base64):
        return self.image_service.get_image_pixmap(image_base64)

    def get_images(self):
        return self.image_service.images