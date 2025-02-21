from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from utils.add_button import add_button
from assets.styles.styles import title_view_stylesheet

class CCIMAR10View(QMainWindow):
    # Sinais para comunicação com o controlador
    messageAlert = pyqtSignal()

    def __init__(self, icons, model, database_path, parent=None):
        super().__init__(parent)
        self.icons = icons
        self.model = model
        self.database_path = database_path
        # Configura a interface de usuário
        self.setup_ui()

    def setup_ui(self):
        # Cria o widget principal e layout principal
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        title_layout = QHBoxLayout()
        label_title = QLabel("Departamento de Auditoria Interna (CCIMAR-10)", self)
        label_title.setStyleSheet(title_view_stylesheet())
        title_layout.addWidget(label_title)
        title_layout.addStretch()

        self.main_layout.addLayout(title_layout)
        
        top_layout = QHBoxLayout()
        self.setup_buttons(top_layout)
        self.main_layout.addLayout(top_layout)

    def setup_buttons(self, layout):
        add_button("Mensagem", "mensagem", self.messageAlert, layout, self.icons, tooltip="Adicionar um novo item")  # Alteração aqui
        add_button("API", "api", self.messageAlert, layout, self.icons, tooltip="Excluir o item selecionado")
        add_button("Abrir Tabela", "excel", self.messageAlert, layout, self.icons, tooltip="Salva o dataframe em um arquivo Excel")