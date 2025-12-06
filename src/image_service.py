import base64
from PyQt6.QtCore import QObject, pyqtSignal, QBuffer, QByteArray, QIODevice
from PyQt6.QtGui import QPixmap

class ImageService(QObject):
    images_updated = pyqtSignal(list)

    def __init__(self, settings_manager):
        super().__init__()
        self.settings = settings_manager

        self.images = settings_manager.get('images')
        self.max_size = settings_manager.get('max_images_size')

    def add_image(self, pixmap):
        image_base64 = self.pixmap_to_base64(pixmap)
        if image_base64 and image_base64 not in self.images:
            new_images = [image_base64] + self.images
            if len(new_images) > self.max_size:
                new_images = new_images[:self.max_size]
            self._update_images(new_images)
            return True
        return False

    def remove_image(self, image_base64):
        if image_base64 in self.images:
            new_images = [img for img in self.images if img != image_base64]
            self._update_images(new_images)
            return True
        return False

    def clear_images(self):
        self._update_images([])

    def update_max_size(self, new_size):
        self.max_size = new_size
        if len(self.images) > self.max_size:
            self.images = self.images[:self.max_size]
            self._update_images(self.images)

    def get_image_pixmap(self, image_base64):
        return self.base64_to_pixmap(image_base64)

    def _update_images(self, images):
        self.images = images
        self.settings.set('images', images)
        self.images_updated.emit(images)

    @staticmethod
    def pixmap_to_base64(pixmap):
        if pixmap.isNull():
            return None

        try:
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)

            if not buffer.open(QIODevice.OpenModeFlag.WriteOnly):
                return None

            success = pixmap.save(buffer, "PNG", quality=100)
            buffer.close()

            if not success:
                return None

            if byte_array.isEmpty():
                return None

            base64_data = base64.b64encode(byte_array.data()).decode('utf-8')
            return f'data:image/png;base64,{base64_data}'

        except Exception:
            return None

    @staticmethod
    def base64_to_pixmap(base64_str):
        try:
            if ',' in base64_str:
                base64_str = base64_str.split(',')[1]

            image_data = base64.b64decode(base64_str)
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            return pixmap
        except Exception:
            return QPixmap()