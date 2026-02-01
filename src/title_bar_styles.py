def get_title_bar_styles(theme):
    text_color = "white"
    close_color = "#ff6b6b"

    if theme["name"] == "Светлая":
        title_bar_bg = "#0078d4"
        text_color = "black"
    elif theme["name"] == "Тёмная":
        title_bar_bg = "#1a1a1a"
    elif theme["name"] == "Голубая":
        title_bar_bg = "#0066cc"
        text_color = "black"
    elif theme["name"] == "Градиент":
        title_bar_bg = "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #f093fb)"
    else:
        title_bar_bg = theme.get("accent", "#0078d4")

    menu_styles = f"""
        QMenu#mainMenu {{
            background-color: {theme["secondary_background"]};
            color: {theme["text"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            padding: 5px;
            min-width: 200px;
        }}

        QMenu#mainMenu::item {{
            padding: 8px 15px;
            margin: 2px 0;
            border-radius: 3px;
            color: {theme["text"]};
        }}

        QMenu#mainMenu::item:selected {{
            background-color: {theme["accent"]};
            color: white;
        }}

        QMenu#mainMenu QMenu {{
            background-color: {theme["secondary_background"]};
            color: {theme["text"]};
            border: 1px solid {theme["border"]};
            border-radius: 4px;
            margin: 5px 0 5px 5px;
        }}

        QMenu#mainMenu QMenu::item {{
            padding: 6px 25px 6px 15px;
            margin: 2px 0;
            border-radius: 3px;
            color: {theme["text"]};
        }}

        QMenu#mainMenu QMenu::item:selected {{
            background-color: {theme["accent"]};
            color: white;
        }}

        QMenu#mainMenu::right-arrow {{
            image: none;
            width: 8px;
            height: 8px;
            border-right: 2px solid {theme["text"]};
            border-bottom: 2px solid {theme["text"]};
            transform: rotate(-45deg);
            margin-right: 10px;
        }}

        QMenu#mainMenu::right-arrow:selected {{
            border-color: white;
        }}

        QMenu#mainMenu::separator {{
            height: 1px;
            background: {theme["border"]};
            margin: 5px 10px;
        }}
    """

    return f"""
        CustomTitleBar {{
            background: {title_bar_bg};
            border-bottom: 1px solid {theme["border"]};
            border-radius: 8px 8px 0 0;
        }}

        CustomTitleBar QLabel {{
            color: {text_color};
            font-weight: bold;
            font-size: 13px;
            padding-left: 5px;
        }}

        CustomTitleBar QPushButton {{
            color: {text_color};
        }}

        CustomTitleBar QPushButton#menuBtn {{
            background-color: transparent;
            border: none;
            border-radius: 3px;
            min-width: 30px;
            min-height: 30px;
            font-size: 20px;
            color: {text_color};
            padding: 0;
        }}

        CustomTitleBar QPushButton#menuBtn:hover {{
            background-color: rgba(255, 255, 255, 0.2);
        }}

        CustomTitleBar QPushButton#menuBtn:pressed {{
            background-color: rgba(255, 255, 255, 0.3);
        }}

        CustomTitleBar QPushButton#minimizeBtn {{
            background-color: transparent;
            border: none;
            border-radius: 3px;
            color: {text_color};
            font-size: 28px;
            font-weight: normal;
            min-width: 30px;
            min-height: 30px;
            padding: 0;
        }}

        CustomTitleBar QPushButton#maximizeBtn {{
            background-color: transparent;
            border: none;
            border-radius: 3px;
            color: {text_color};
            font-size: 20px;
            font-weight: normal;
            min-width: 30px;
            min-height: 30px;
            padding: 0;
        }}

        CustomTitleBar QPushButton#closeBtn {{
            background-color: transparent;
            border: none;
            border-radius: 3px;
            color: {text_color};
            font-size: 22px;
            font-weight: normal;
            min-width: 30px;
            min-height: 30px;
            padding: 0;
        }}

        CustomTitleBar QPushButton#minimizeBtn:hover,
        CustomTitleBar QPushButton#maximizeBtn:hover {{
            background-color: rgba(255, 255, 255, 0.2);
        }}

        CustomTitleBar QPushButton#minimizeBtn:pressed,
        CustomTitleBar QPushButton#maximizeBtn:pressed {{
            background-color: rgba(255, 255, 255, 0.3);
        }}

        CustomTitleBar QPushButton#closeBtn:hover {{
            background-color: {close_color};
            color: white;
        }}

        {menu_styles}

        QMainWindow#settings_window CustomTitleBar {{
            background: {title_bar_bg};
        }}
    """