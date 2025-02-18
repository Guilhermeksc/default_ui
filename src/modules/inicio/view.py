from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from pathlib import Path
from paths import ICONS_DIR
from assets.styles.styles import title_view_stylesheet

class InicioWidget(QWidget):
    def __init__(self, icons, parent=None):
        super().__init__(parent)
        self.icons = icons
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        # Configurações de expansão para ajustar ao tamanho da janela
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Título do projeto
        self.title_label = QLabel("    CCIMAR-360")
        self.title_label.setStyleSheet(title_view_stylesheet())

        # Sinopse do projeto
        self.synopsis_label = QLabel(
            "CCIMAR360 é um projeto em desenvolvimento para automatizar processos repetitivos relacionados "
            "as atividades de auditoria do Centro de Controle Interno da Marinha (CCIMAR). Com um foco na otimização e eficiência, o projeto oferece ferramentas "
            "para manipulação de documentos PDF, DOCX e XLSX, geração de relatórios, e automação de tarefas via RPA. "
            "O objetivo principal é melhorar a qualidade de vida no trabalho, minimizando erros e reduzindo a quantidade "
            "de cliques necessários para completar uma tarefa."
        )
        self.synopsis_label.setAlignment(Qt.AlignmentFlag.AlignJustify)
        self.synopsis_label.setWordWrap(True)
        self.synopsis_label.setStyleSheet("font-size: 16px; padding: 10px;")

        # Adiciona os widgets ao layout
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.synopsis_label)

        # Agora cria um QHBoxLayout para os módulos e a imagem
        modules_and_image_layout = QHBoxLayout()

        # Layout à esquerda para os módulos
        self.modules_layout = QVBoxLayout()

        # Módulos para Data Science
        self.add_module(
            "  Aquisição de Dados",
            "Responsável por coletar dados de sensores, APIs e outras fontes relevantes.",
            "initdatacollection.png"  # Certifique-se de que esse ícone esteja disponível em ICONS_DIR
        )
        self.add_module(
            "  Pré-processamento e Limpeza",
            "Normaliza, trata valores faltantes e transforma os dados para análises futuras.",
            "initdataprocessing.png"
        )
        self.add_module(
            "  Análise Exploratória",
            "Gera estatísticas, gráficos e insights iniciais para orientar as modelagens.",
            "initexploration.png"
        )
        self.add_module(
            "  Visualização e Relatórios",
            "Cria dashboards interativos e relatórios automatizados para suporte à decisão.",
            "initreport.png"
        )

        # Adiciona o layout dos módulos à esquerda no layout horizontal
        modules_and_image_layout.addLayout(self.modules_layout)

        # Adiciona o layout horizontal de módulos e imagem ao layout principal vertical
        self.layout.addLayout(modules_and_image_layout)

        # Contato
        self.contact_label = QLabel(
            'Para mais informações, entre em contato pelo e-mail: <a href="mailto:siqueira.campos@marinha.mil.br">siqueira.campos@marinha.mil.br</a>'
        )
        self.contact_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contact_label.setOpenExternalLinks(True)
        self.contact_label.setStyleSheet("font-size: 16px; padding: 10px;")

        # Adiciona o contato ao final
        self.layout.addWidget(self.contact_label)

        # Adiciona um espaço flexível para empurrar o contato para o final
        self.layout.addStretch()

    def add_module(self, title, description, icon_name):
        """Adiciona um módulo com ícone, título e descrição alinhados corretamente."""
        icon = self.icons.get(icon_name.split('.')[0], QIcon())
        module_layout = QHBoxLayout()

        # Define espaçamento 0,0,0,0
        module_layout.setContentsMargins(0, 0, 0, 0)
        module_layout.setSpacing(0)

        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(40, 40))

        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(0)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_layout.addWidget(title_label)

        description_label = QLabel(description)
        description_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignJustify)
        description_label.setWordWrap(True)
        description_label.setStyleSheet("font-size: 16px; padding-left: 5px;")
        title_layout.addWidget(description_label)

        module_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignRight)
        module_layout.addLayout(title_layout)

        module_widget = QWidget()
        module_widget.setLayout(module_layout)

        self.modules_layout.addWidget(module_widget)