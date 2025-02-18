from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import os
import subprocess
from docx import Document
from paths import TEMPLATE_TEST_PATH


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
                padding: 5px;
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
            ("Teste", self.show_teste_widget),
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

    def show_teste_widget(self):
        self.clear_content()
        # Widget principal para o conteúdo da scroll area
        teste_widget = QWidget()
        layout = QVBoxLayout(teste_widget)
        # Título
        title = QLabel("Teste")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #4E648B")
        layout.addWidget(title)

        # Campos de entrada
        self.pasta_input = QLineEdit()
        self.pasta_input.setPlaceholderText("Nome da Pasta")
        layout.addWidget(self.pasta_input)
        
        self.setor_input = QLineEdit()
        self.setor_input.setPlaceholderText("Setor Responsável")
        layout.addWidget(self.setor_input)
        
        self.observacao_input = QLineEdit()
        self.observacao_input.setPlaceholderText("Observação")
        layout.addWidget(self.observacao_input)

        # Botões
        self.btn_criar_pasta = QPushButton("Criar Pasta")
        self.btn_criar_pasta.clicked.connect(self.criar_pasta)
        layout.addWidget(self.btn_criar_pasta)
        
        self.btn_criar_pasta_docx = QPushButton("Criar Pasta e Arquivos DOCX")
        self.btn_criar_pasta_docx.clicked.connect(self.criar_pasta_e_docx)
        layout.addWidget(self.btn_criar_pasta_docx)
        
        self.btn_criar_pasta_pdf = QPushButton("Criar Pasta e Arquivos PDF")
        self.btn_criar_pasta_pdf.clicked.connect(self.criar_pasta_e_pdf)
        layout.addWidget(self.btn_criar_pasta_pdf)

        # Adiciona o scroll area ao layout principal
        self.content_layout.addWidget(teste_widget)


    def criar_pasta(self):
        nome_pasta = self.pasta_input.text().strip()
        if nome_pasta:
            caminho_pasta = os.path.join(os.path.expanduser("~/Desktop"), nome_pasta)
            os.makedirs(caminho_pasta, exist_ok=True)
            try:
                if os.name == "nt":  # Windows
                    os.startfile(caminho_pasta)
                elif os.name == "posix":  # Linux/Mac
                    subprocess.run(["xdg-open", caminho_pasta])
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao abrir a pasta: {e}")

    def criar_pasta_e_docx(self):
        self.criar_pasta()
        nome_pasta = self.pasta_input.text().strip()
        setor_responsavel = self.setor_input.text().strip()
        observacao = self.observacao_input.text().strip()
        caminho_pasta = os.path.join(os.path.expanduser("~/Desktop"), nome_pasta)
        
        if nome_pasta:
            try:
                doc = Document(TEMPLATE_TEST_PATH)
                for var in doc.paragraphs:
                    if "{{setor_responsavel}}" in var.text:
                        var.text = var.text.replace("{{setor_responsavel}}", setor_responsavel)
                    if "{{observacao}}" in var.text:
                        var.text = var.text.replace("{{observacao}}", observacao)

                doc_path = os.path.join(caminho_pasta, "documento.docx")
                doc.save(doc_path)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao criar o arquivo DOCX: {e}")

    def criar_pasta_e_pdf(self):
        self.criar_pasta_e_docx()  # Criar DOCX primeiro
        nome_pasta = self.pasta_input.text().strip()
        caminho_pasta = os.path.join(os.path.expanduser("~/Desktop"), nome_pasta)
        
        if nome_pasta:
            docx_path = os.path.join(caminho_pasta, "documento.docx")
            pdf_path = os.path.join(caminho_pasta, "documento.pdf")
            
            # Convert DOCX to PDF (necessário o LibreOffice ou outra solução instalada)
            try:
                os.system(f'libreoffice --headless --convert-to pdf "{docx_path}" --outdir "{caminho_pasta}"')
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao converter para PDF: {e}")