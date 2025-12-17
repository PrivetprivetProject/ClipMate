THEMES = {
    "light": {
        "name": "Светлая",
        "primary_background": "#f5f5f5",
        "secondary_background": "#ffffff",
        "border": "#cccccc",
        "text": "#333333",
        "accent": "#0078d4",
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545"
    },
    "dark": {
        "name": "Тёмная",
        "primary_background": "#2b2b2b",
        "secondary_background": "#3c3c3c",
        "border": "#555555",
        "text": "#e0e0e0",
        "accent": "#569cd6",
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545"
    },
    "blue": {
        "name": "Голубая",
        "primary_background": "#e6f2ff",
        "secondary_background": "#ffffff",
        "border": "#99ccff",
        "text": "#003366",
        "accent": "#0066cc",
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545"
    },
    "gradient": {
        "name": "Градиент",
        "primary_background": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb)",
        "secondary_background": "rgba(255, 255, 255, 0.95)",
        "border": "rgba(0, 120, 212, 0.3)",
        "text": "#333333",
        "accent": "#0078d4",
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545"
    }
}

AVAILABLE_THEMES = [
    ("light", "Светлая"),
    ("dark", "Тёмная"),
    ("blue", "Голубая"),
    ("gradient", "Градиент")
]


def get_theme_styles(theme_name="light"):
    theme = THEMES.get(theme_name, THEMES["light"])

    settings_backgrounds = {
        "light": "#e6f2ff",
        "dark": "#1a1a1a",
        "blue": "#c2e0ff",
        "gradient": "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4facfe, stop:1 #00f2fe)"
    }

    settings_bg = settings_backgrounds.get(theme_name, theme["primary_background"])

    return f"""
        /* Основные окна */
        QMainWindow {{
            background: {theme["primary_background"]};
            border: 1px solid {theme["border"]};
            border-radius: 8px;
        }}

        QMainWindow#settings_window {{
            background: {settings_bg};
            border: 1px solid {theme["border"]};
            border-radius: 8px;
        }}

        QWidget#central_widget,
        QWidget#container,
        QWidget#main_container,
        QWidget#settings_container,
        QWidget#content_container,
        QWidget#settings_content {{
            background: transparent;
        }}

        QTabWidget::pane {{
            background: {theme["secondary_background"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
        }}

        QTabBar::tab {{
            background: {theme["secondary_background"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px 4px 0 0;
            padding: 8px 12px;
            color: {theme["text"]};
            margin-right: 2px;
        }}

        QTabBar::tab:selected {{
            background: {theme["accent"]};
            color: white;
        }}

        QTabBar::tab:hover {{
            background: {theme["accent"]}20;
        }}

        QListWidget {{
            background: {theme["secondary_background"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            color: {theme["text"]};
            font-size: 12px;
        }}

        QListWidget::item {{
            padding: 6px;
            border-bottom: 1px solid {theme["border"]}40;
        }}

        QListWidget::item:selected {{
            background: {theme["accent"]};
            color: white;
        }}

        QTextEdit {{
            background: {theme["secondary_background"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            color: {theme["text"]};
            font-size: 12px;
            selection-background-color: {theme["accent"]};
        }}

        QLineEdit {{
            background: {theme["secondary_background"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            color: {theme["text"]};
            padding: 6px;
            font-size: 12px;
        }}

        QLineEdit:focus {{
            border: 2px solid {theme["accent"]};
            padding: 5px;
        }}

        QLabel {{
            color: {theme["text"]};
            font-size: 12px;
        }}

        QLabel[title="tab"] {{
            font-size: 14px;
            font-weight: bold;
            padding: 8px;
            background: {theme["secondary_background"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
        }}

        QLabel[status="success"] {{
            color: {theme["success"]};
        }}

        QLabel[status="warning"] {{
            color: {theme["warning"]};
        }}

        QLabel[status="error"] {{
            color: {theme["error"]};
        }}

        QGroupBox {{
            color: {theme["text"]};
            border: 1px solid {theme["border"]};
            border-radius: 6px;
            margin-top: 10px;
            font-weight: bold;
            background: {theme["secondary_background"]};
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            background: {theme["secondary_background"]};
            border-radius: 4px;
        }}

        QComboBox {{
            background: {theme["secondary_background"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            color: {theme["text"]};
            padding: 6px;
            min-height: 24px;
        }}

        QComboBox:hover {{
            border: 1px solid {theme["accent"]};
        }}

        QComboBox::drop-down {{
            border: none;
            border-left: 1px solid {theme["border"]};
            width: 20px;
        }}

        QComboBox::down-arrow {{
            image: none;
        }}

        QPushButton {{
            background: {theme["accent"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            color: white;
            padding: 6px 12px;
            font-size: 12px;
        }}

        QPushButton:hover {{
            background: {theme["accent"]}dd;
        }}

        QPushButton:pressed {{
            background: {theme["accent"]}bb;
        }}

        QMenu {{
            background: {theme["secondary_background"]};
            color: {theme["text"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            padding: 5px;
        }}

        QMenu::item {{
            padding: 6px 25px 6px 20px;
            border-radius: 3px;
            margin: 2px 0;
            color: {theme["text"]};
        }}

        QMenu::item:selected {{
            background: {theme["accent"]};
            color: white;
        }}

        QMenu::separator {{
            height: 1px;
            background: {theme["border"]};
            margin: 5px 10px;
        }}
    """