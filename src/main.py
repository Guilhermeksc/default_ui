from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from paths import *
from utils.icon_loader import load_icons
from assets.styles.styles import get_menu_button_style, get_menu_button_activated_style
from modules.widgets import *
from config.config_widget import ConfigManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.icons = load_icons()
        self.buttons = {}
        self.active_button = None
        self.inicio_widget = None
        self.setup_ui()
        self.open_initial_page()

    # ====== SETUP DA INTERFACE ======
    def setup_ui(self):
        """Configura a interface principal da aplicação."""
        self.configure_window()
        self.setup_central_widget()
        self.setup_menu()
        self.setup_content_area()

    def configure_window(self):
        """Configurações básicas da janela principal."""
        self.setWindowTitle("CCIMAR360 - Ciência de Dados Aplicada à Auditoria")
        self.setWindowIcon(self.icons["data-science"])        
        # Posiciona a janela no canto superior esquerdo
        screen_geometry = self.screen().geometry()
        self.move(screen_geometry.left(), screen_geometry.top())
        
    def setup_central_widget(self):
        """Define o widget central e layout principal."""
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QHBoxLayout(self.central_widget)
        self.central_layout.setSpacing(0)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        
    def setup_menu(self):
        """Configura o menu lateral com botões de ícone que mudam de cor ao hover e adiciona tooltips personalizados."""
        self.menu_layout = QVBoxLayout()
        self.menu_layout.setSpacing(0)
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Tooltip personalizado
        self.tooltip_label = QLabel("", self)
        self.tooltip_label.setStyleSheet("""
            background-color: #13141F;
            color: white;
            border: 1px solid #8AB4F7;
            padding: 4px;
            border-radius: 4px;
        """)
        self.tooltip_label.setFont(QFont("Arial", 12))
        self.tooltip_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tooltip_label.setVisible(False)  # Inicialmente oculto

        # Definindo os botões do menu e seus contextos
        self.menu_buttons = [
            ("init", "init_hover", "Página Inicial", self.show_inicio),
            ("number-10-b", "number-10", "Departamento de Auditoria Interna (CCIMAR-10)", self.show_ccimar10),
            ("number-11-b", "number-11", "Divisão de Planejamento e Monitoramento (CCIMAR-11)", self.show_ccimar11),
            ("number-12-b", "number-12", "Divisão de Licitações (CCIMAR-12)", self.show_ccimar12),
            ("number-13-b", "number-13", "Divisão de Execução (CCIMAR-13)", self.show_ccimar13),
            ("number-14-b", "number-14", "Divisão de Pagamento (CCIMAR-14)", self.show_ccimar14),
            ("number-15-b", "number-15", "Divisão de Material (CCIMAR-15)", self.show_ccimar15),
            ("number-16-b", "number-16", "Divisão de Ciência de Dados Aplicada à Auditoria (CCIMAR-16)", self.show_ccimar16),
            ("data_blue", "data", "Utilidades", self.show_ccimar_utils),
            ("config", "config_hover", "Configurações", self.show_config),
        ]

        # Criando os botões e adicionando-os ao layout do menu
        for icon_key, hover_icon_key, tooltip_text, callback in self.menu_buttons:
            button = self.create_icon_button(icon_key, hover_icon_key, icon_key)
            button.clicked.connect(callback)
            button.installEventFilter(self)  # Instala um filtro de evento para gerenciar o tooltip
            button.setProperty("tooltipText", tooltip_text)  # Define o texto do tooltip como propriedade
            self.menu_layout.addWidget(button)
            self.buttons[icon_key] = button 
            
        # Adiciona um espaço flexível para empurrar o ícone para o final
        self.menu_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Adiciona o ícone 360-degrees.png na parte inferior

        icon_label = QLabel(self)
        icon_label.setPixmap(self.icons["360-degrees"].pixmap(40, 40))  # Define o ícone com tamanho 50x50
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_layout.addWidget(icon_label)

        # Cria um widget para o menu e adiciona o layout
        self.menu_widget = QWidget()
        self.menu_widget.setLayout(self.menu_layout)
        self.menu_widget.setStyleSheet("background-color: #13141F;")

        self.central_layout.addWidget(self.menu_widget)
            
    def eventFilter(self, obj, event):
        """Filtra eventos para exibir tooltips personalizados alinhados à direita dos botões do menu e gerenciar ícones."""
        if isinstance(obj, QPushButton):
            # Evento de entrada do mouse no botão
            if event.type() == QEvent.Type.Enter and obj in self.buttons.values():
                tooltip_text = obj.property("tooltipText")
                if tooltip_text:
                    self.tooltip_label.setText(tooltip_text)
                    self.tooltip_label.adjustSize()

                    # Posição do tooltip alinhada à direita do botão
                    button_pos = obj.mapToGlobal(QPoint(obj.width(), 0))  # Posição global do botão
                    tooltip_x = button_pos.x() + 5  # Ajuste para a direita do botão
                    tooltip_y = button_pos.y() + (obj.height() - self.tooltip_label.height()) // 2  # Centraliza verticalmente
                    self.tooltip_label.move(self.mapFromGlobal(QPoint(tooltip_x, tooltip_y)))  # Converte para coordenadas da janela
                    self.tooltip_label.setVisible(True)

                # Altera o ícone do botão para o estado de hover, se não estiver selecionado
                if not obj.property("isSelected"):
                    obj.setIcon(obj.hover_icon)

            # Evento de saída do mouse do botão
            elif event.type() == QEvent.Type.Leave and obj in self.buttons.values():
                self.tooltip_label.setVisible(False)

                # Retorna o ícone ao estado padrão, se não estiver selecionado
                if not obj.property("isSelected"):
                    obj.setIcon(obj.default_icon)

            # Evento de clique no botão
            elif event.type() == QEvent.Type.MouseButtonPress and obj in self.buttons.values():
                # Desmarca todos os botões e reseta os ícones
                for btn in self.buttons.values():
                    btn.setProperty("isSelected", False)
                    btn.setIcon(btn.default_icon)

                # Marca o botão clicado como selecionado e altera o ícone
                obj.setProperty("isSelected", True)
                obj.setIcon(obj.selected_icon)

        return super().eventFilter(obj, event)        
    
    def create_icon_button(self, icon_key, hover_icon_key, selected_icon_key):
        button = QPushButton()
        button.setIcon(self.icons[icon_key])  # Ícone padrão
        button.setIconSize(QSize(30, 30))
        button.setStyleSheet(get_menu_button_style())
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setFixedSize(50, 50)

        # Armazena os ícones padrão, de hover e de seleção
        button.default_icon = self.icons[icon_key]
        button.hover_icon = self.icons[hover_icon_key]
        button.selected_icon = self.icons[selected_icon_key]
        button.icon_key = icon_key  # Armazena a chave do ícone

        # Propriedade para gerenciar o estado selecionado
        button.setProperty("isSelected", False)

        # Instala o event filter para capturar eventos de hover e selected
        button.installEventFilter(self)

        return button

    def set_active_button(self, button):
        """Define o botão ativo e altera o ícone para o estado hover permanente."""
        # Reseta o estilo do botão anteriormente ativo
        if self.active_button and self.active_button != button:
            self.active_button.setIcon(self.active_button.default_icon)
            self.active_button.setStyleSheet(get_menu_button_style())

        # Aplica o estilo de botão ativo
        button.setIcon(button.hover_icon)
        button.setStyleSheet(get_menu_button_activated_style())
        self.active_button = button 

    # ====== MÓDULOS ======
    def show_ccimar10(self):
        self.clear_content_area()        
        # Instancia o modelo com o caminho do banco de dados
        self.ccimar10_model = CCIMAR10Model(CCIMAR10_PATH)        
        # Configura o modelo SQL
        sql_model = self.ccimar10_model.setup_model("ccimar10", editable=True)        
        # Cria a View e passa o modelo SQL e o caminho do banco de dados
        self.ccimar10_view = CCIMAR10View(self.icons, sql_model, self.ccimar10_model.database_manager.db_path)
        # Cria o controlador e passa o widget e o modelo
        self.ccimar10_controller = CCIMAR10Controller(self.icons, self.ccimar10_view, self.ccimar10_model)
        # Adiciona o widget de Dispensa Eletrônica na área de conteúdo
        self.content_layout.addWidget(self.ccimar10_view)
        self.set_active_button(self.buttons["number-10-b"])

    # def show_ccimar11(self):
    #     self.clear_content_area()        
    #     self.ccimar11_model = CCIMAR11Model(CCIMAR11_PATH)
    #     sql_model = self.ccimar11_model.setup_model("ccimar11_db", editable=True)
    #     self.ccimar11_view = CCIMAR11View(self.icons, sql_model, self.ccimar11_model.database_manager.db_path)
    #     self.ccimar11_controller = CCIMAR11Controller(self.icons, self.ccimar11_view, self.ccimar11_model)
    #     self.content_layout.addWidget(self.ccimar11_view)
    #     self.set_active_button(self.buttons["number-11-b"])

    def show_ccimar11(self):
        self.clear_content_area()
        
        print("Initializing CCIMAR11 Model...")  
        self.ccimar11_model = CCIMAR11Model(CCIMAR11_PATH)
        print("Model initialized successfully.")

        sql_model = self.ccimar11_model.setup_model("ccimar11", editable=True)
        print("SQL Model set up successfully.")

        print(f"Database path: {self.ccimar11_model.database_manager.db_path}")

        self.ccimar11_view = CCIMAR11View(self.icons, sql_model, self.ccimar11_model.database_manager.db_path)
        print("CCIMAR11 View initialized.")

        self.ccimar11_controller = CCIMAR11Controller(self.icons, self.ccimar11_view, self.ccimar11_model)
        print("CCIMAR11 Controller initialized.")

        self.content_layout.addWidget(self.ccimar11_view)
        self.set_active_button(self.buttons["number-11-b"])

        print("CCIMAR11 module loaded successfully.")


    def show_ccimar12(self):
        self.clear_content_area()        
        self.ccimar12_model = CCIMAR12Model(CCIMAR12_PATH)
        sql_model = self.ccimar12_model.setup_model("ccimar12", editable=True)
        self.ccimar12_view = CCIMAR12View(self.icons, sql_model, self.ccimar12_model.database_manager.db_path)
        self.ccimar12_controller = CCIMAR12Controller(self.icons, self.ccimar12_view, self.ccimar12_model)
        self.content_layout.addWidget(self.ccimar12_view)
        self.set_active_button(self.buttons["number-12-b"])

    def show_ccimar13(self):
        self.clear_content_area()        
        self.ccimar13_model = CCIMAR13Model(CCIMAR13_PATH)
        sql_model = self.ccimar13_model.setup_model("ccimar13", editable=True)
        self.ccimar13_view = CCIMAR13View(self.icons, sql_model, self.ccimar13_model.database_manager.db_path)
        self.ccimar13_controller = CCIMAR13Controller(self.icons, self.ccimar13_view, self.ccimar13_model)
        self.content_layout.addWidget(self.ccimar13_view)
        self.set_active_button(self.buttons["number-13-b"])

    def show_ccimar14(self):
        self.clear_content_area()        
        self.ccimar14_model = CCIMAR14Model(CCIMAR14_PATH)
        sql_model = self.ccimar14_model.setup_model("ccimar14", editable=True)
        self.ccimar14_view = CCIMAR14View(self.icons, sql_model, self.ccimar14_model.database_manager.db_path)
        self.ccimar14_controller = CCIMAR14Controller(self.icons, self.ccimar14_view, self.ccimar14_model)
        self.content_layout.addWidget(self.ccimar14_view)
        self.set_active_button(self.buttons["number-14-b"])

    def show_ccimar15(self):
        self.clear_content_area()        
        self.ccimar15_model = CCIMAR15Model(CCIMAR15_PATH)
        sql_model = self.ccimar15_model.setup_model("ccimar15", editable=True)
        self.ccimar15_view = CCIMAR15View(self.icons, sql_model, self.ccimar15_model.database_manager.db_path)
        self.ccimar15_controller = CCIMAR15Controller(self.icons, self.ccimar15_view, self.ccimar15_model)
        self.content_layout.addWidget(self.ccimar15_view)
        self.set_active_button(self.buttons["number-15-b"])
                                               
    def show_ccimar16(self):
        self.clear_content_area()        
        self.ccimar16_model = CCIMAR16Model(CCIMAR16_PATH)
        sql_model = self.ccimar16_model.setup_model("ccimar16", editable=True)
        self.ccimar16_view = CCIMAR16View(self.icons, sql_model, self.ccimar16_model.database_manager.db_path)
        self.ccimar16_controller = CCIMAR16Controller(self.icons, self.ccimar16_view, self.ccimar16_model)
        self.content_layout.addWidget(self.ccimar16_view)
        self.set_active_button(self.buttons["number-16-b"])

    def show_ccimar_utils(self):
        self.clear_content_area()        
        self.utils_model = UtilsModel(CCIMAR_UTIL_PATH)
        sql_model = self.utils_model.setup_model("ccimar_utils", editable=True)
        self.utils_view = UtilsView(self.icons, sql_model, self.utils_model.database_manager.db_path)
        self.utils_controller = UtilsController(self.icons, self.utils_view, self.utils_model)
        self.content_layout.addWidget(self.utils_view)
        self.set_active_button(self.buttons["number-16-b"])

    def show_config(self):
        self.clear_content_area()
        # Instanciar o ConfigManager com os ícones
        self.config_manager = ConfigManager(self.icons, self)
        # Adicionar o ConfigManager à área de conteúdo
        self.content_layout.addWidget(self.config_manager)
        # Define o botão correspondente como ativo
        self.set_active_button(self.buttons["config"])

    def show_inicio(self):
        self.clear_content_area()
        self.inicio_widget = InicioWidget(self.icons)
        self.content_layout.addWidget(self.inicio_widget)
        # Define o botão "init" como o ativo (correspondente ao botão inicial)
        self.set_active_button(self.buttons["init"])    
        
    def open_initial_page(self):
        """Abre a página inicial da aplicação."""
        self.clear_content_area()
        # Verifica se inicio_widget foi iniciado corretamente, caso contrário, chama show_inicio
        if not self.inicio_widget :
            self.show_inicio()
        else:
            self.content_layout.addWidget(self.inicio_widget )

        # Define o botão "init" como ativo
        self.set_active_button(self.buttons["init"]) 
        
    # ====== ÁREA DE CONTEÚDO ======

    def setup_content_area(self):
        """Configura a área principal para exibição do conteúdo sem afetar os elementos internos."""
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.content_image_label = QLabel(self.central_widget)
        self.content_image_label.hide()
        self.content_layout.addWidget(self.content_image_label)

        # Usar QFrame para melhor controle de estilo
        self.content_widget = QFrame()
        self.content_widget.setObjectName("contentWidget")
        self.content_widget.setLayout(self.content_layout)
        self.content_widget.setMinimumSize(1050, 700)
        self.content_widget.setFrameStyle(QFrame.Shape.NoFrame)  # Remove qualquer borda padrão

        # Aplicar estilo apenas no background do content_widget
        self.content_widget.setStyleSheet("""
            QFrame#contentWidget {
                background-color: #181928;
            }
        """)

        self.central_layout.addWidget(self.content_widget)


    def clear_content_area(self, keep_image_label=False):
        """Remove todos os widgets da área de conteúdo, exceto a imagem opcional."""
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget and (widget is not self.content_image_label or not keep_image_label):
                widget.setParent(None)
                    
    # ====== EVENTO DE FECHAMENTO DA JANELA ======

    def closeEvent(self, event):
        """Solicita confirmação ao usuário antes de fechar a janela."""
        reply = QMessageBox.question(
            self, 'Confirmar Saída', "Você realmente deseja fechar o aplicativo?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        event.accept() if reply == QMessageBox.StandardButton.Yes else event.ignore()
                    
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
