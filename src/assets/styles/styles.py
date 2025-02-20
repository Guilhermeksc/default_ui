from PyQt6.QtGui import QIcon, QPixmap

def get_menu_button_style():
    return """
        QPushButton {
            background-color: transparent;
            font-weight: bold;
            font-size: 16px;
            text-align: left;
            border: 1px solid transparent;
            border-left: 2px solid transparent; 
            border-radius: 0px;
            padding: 5px;
            margin: 0px; 
        }
        QPushButton:hover {
            background-color: #454A63;
            border-left: 2px solid transparent;
            color: white;
            border-radius: 0px;
            padding: 5px;
        }
    """

def get_menu_button_activated_style():
    return """
        QPushButton {
            background-color: #454A63;
            color: white;
            font-weight: bold;
            font-size: 16px;
            text-align: left;
            border: 1px solid #454A63;
            border-left: 2px solid #F3F3F3;
            border-radius: 0px;
            padding: 5px;
            margin: 0px; 
        }
    """

def table_view_stylesheet() -> str:
    return """
    QTableView {
        font-size: 14px;
        padding: 4px;
        border: 1px solid #8AB4F7;
        border-radius: 6px;
        gridline-color: #3C3C5A;
    }
    """

def title_view_stylesheet() -> str:
    return """
    QLabel {
        font-size: 20px;
        font-weight: bold;
        color: #4E648B;
    }
    """
