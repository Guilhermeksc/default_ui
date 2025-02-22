from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QLabel, QFrame
from PyQt6.QtCore import pyqtSignal
from .menu.treeview_menu import TreeMenu
from .menu.menu_callbacks import *

class CCIMAR11View(QMainWindow):
    teste = pyqtSignal()

    def __init__(self, icons, model, database_model, parent=None):
        super().__init__(parent)
        self.icons = icons
        self.model = model
        self.database_model = database_model
        self.document = None
        self.current_content_layout = None
        self.setup_ui()

    def setup_ui(self):
        """Configures the layout with a sidebar menu using TreeMenu."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar menu using TreeMenu
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)

        label = QLabel("CCIMAR11", self)
        label.setStyleSheet("color: #FFF; font-size: 24px")
        sub_label = QLabel("Planejamento e Monitoramento", self)
        sub_label.setStyleSheet("color: #FFF; font-size: 12px")

        menu_layout.addWidget(label)
        menu_layout.addWidget(sub_label)
        
        line = QFrame(self)
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #FFF;")
        menu_layout.addWidget(line)
        
        spacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        menu_layout.addItem(spacer)
        
        self.tree_menu = TreeMenu(self.icons, owner=self)
        menu_layout.addWidget(self.tree_menu)

        menu_widget = QWidget()
        menu_widget.setLayout(menu_layout)
        menu_widget.setStyleSheet("background-color: #181928;")
        main_layout.addWidget(menu_widget, stretch=1)

        # Content area with QFrame for background color
        self.content_widget = QFrame()  # ✅ Use QFrame for background styling
        self.content_widget.setStyleSheet("""
            QFrame { 
                background-color: #44475A; 
                border-radius: 0px; 
            }
        """)
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)  # ✅ Remove all margins
        self.content_layout.setSpacing(0)  # ✅ Remove extra spacing

        main_layout.addWidget(self.content_widget, stretch=4)

    def clear_content(self):
        """Clears the current content inside the content widget."""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def clear_layout(self, layout):
        """Recursively clears a layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
