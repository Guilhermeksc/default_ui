from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from pathlib import Path
from paths import ICONS_DIR, CCIMAR360_PATH
from assets.styles.styles import title_view_stylesheet

class InicioWidget(QWidget):
    def __init__(self, icons, parent=None):
        super().__init__(parent)
        self.icons = icons
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # --- Image Label ---
        self.image_label = QLabel(self)
        pixmap = QPixmap(str(CCIMAR360_PATH))
        self.image_label.setPixmap(pixmap.scaledToWidth(250, Qt.TransformationMode.SmoothTransformation))  # Resize width to 250px
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Centering the image
        image_layout = QHBoxLayout()
        image_layout.addStretch()
        image_layout.addWidget(self.image_label)
        image_layout.addStretch()

        self.layout.addLayout(image_layout)

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
        self.layout.addWidget(self.synopsis_label)


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