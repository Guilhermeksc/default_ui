from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from utils.search_bar import setup_search_bar, MultiColumnFilterProxyModel
from utils.add_button import add_button
from assets.styles.styles import table_view_stylesheet, title_view_stylesheet
import pandas as pd

class CCIMAR16View(QMainWindow):
    # Sinais para comunicação com o controlador
    messageAlert = pyqtSignal()
    apiCheck = pyqtSignal()
    openTable = pyqtSignal()
    loadData = pyqtSignal(str)
    rowDoubleClicked = pyqtSignal(dict)
    request_consulta_api = pyqtSignal(str, str, str, str, str)
    
    def __init__(self, icons, model, database_path, parent=None):
        super().__init__(parent)
        self.icons = icons
        self.model = model
        self.database_path = database_path

        # Configura a interface de usuário
        self.setup_ui()
        self.current_content_layout = None

    def setup_ui(self):
        """Configura o layout de configuração com um menu lateral."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Menu lateral
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)

        # Botões do menu lateral
        button_style = """
            QPushButton {
                border: none;
                color: white;
                font-size: 16px; 
                text-align: center;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #3A3B47; 
            }
            QPushButton:checked {
                background-color: #202124; 
                font-weight: bold;
            }
        """

        buttons = [
            ("Ofício do CCIMAR-20", self.show_oficio_ccimar20_widget),
            ("Gerar Notas", self.show_gerar_notas_widget),
            ("Consultas do Airflow", self.show_gerar_notas_widget),
            ("Relatório SGM", self.show_gerar_notas_widget),
            ("Relatório CCIMAR-11", self.show_gerar_notas_widget),
            ("Relatório COFAMAR", self.show_gerar_notas_widget),
            ("Gerar Nota com Cálculo Total", self.show_gerar_notas_widget),
            ("Notas Monitoradas", self.show_gerar_notas_widget),
            ("AUDCONT - Notas Vencidas", self.show_gerar_notas_widget),
        ]

        self.config_menu_buttons = []

        for text, callback in buttons:
            button = QPushButton(text)
            button.setCheckable(True)
            button.setStyleSheet(button_style)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(callback)
            button.clicked.connect(lambda _, b=button: self.set_selected_button(b))
            menu_layout.addWidget(button)
            self.config_menu_buttons.append(button)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        menu_layout.addItem(spacer)

        menu_widget = QWidget()
        menu_widget.setLayout(menu_layout)
        menu_widget.setStyleSheet("background-color: #181928;")
        main_layout.addWidget(menu_widget, stretch=1)

        # Área de conteúdo
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)

        main_layout.addWidget(self.content_widget, stretch=4)

    def set_selected_button(self, selected_button):
        """Define o botão selecionado no menu lateral."""
        for button in self.config_menu_buttons:
            button.setChecked(False)
        selected_button.setChecked(True)

    def clear_content(self):
        """Limpa o layout atual do content_widget."""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def clear_layout(self, layout):
        """Recursivamente limpa um layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def show_oficio_ccimar20_widget(self):
        self.clear_content()
        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        # Widget principal para o conteúdo da scroll area
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        # Título
        title = QLabel("Ofício CCIMAR-20")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4E648B")
        layout.addWidget(title)

        # Configura o widget no scroll area
        scroll_area.setWidget(scroll_widget)

        # Adiciona o scroll area ao layout principal
        self.content_layout.addWidget(scroll_area)

    def show_gerar_notas_widget(self):
        self.clear_content()
        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        # Widget principal para o conteúdo da scroll area
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        # Título
        title = QLabel("Gerar Notas")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4E648B")
        layout.addWidget(title)

        # Configura o widget no scroll area
        scroll_area.setWidget(scroll_widget)

        # Adiciona o scroll area ao layout principal
        self.content_layout.addWidget(scroll_area)