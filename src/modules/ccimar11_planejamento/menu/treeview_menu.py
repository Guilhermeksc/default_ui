# src/modules/ccimar11_planejamento/menu/treeview_menu.py

from PyQt6.QtWidgets import QTreeView, QAbstractItemView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from .menu_callbacks import (  
    show_nota_auditoria_teste1, show_nota_auditoria_teste2,
    show_nota_auditoria_teste3,
    show_oficio_ccimar20_widget, show_gerar_notas_widget,
    show_relatorio_consultas_airflow_widget, show_relatorio_sgm_widget,
    show_relatorio_ccimar11_widget, show_relatorio_cofamar_widget,
    show_relatorio_calculo_total_widget, show_relatorio_notas_monitoradas_widget,
    show_relatorio_audcont_widget, show_teste_widget
)

class TreeMenu(QTreeView):
    def __init__(self, icons, owner, parent=None):
        """
        :param owner: Object that contains the callback methods.
        :param icons: Dictionary containing icons.
        """
        super().__init__(parent)
        self.owner = owner
        self.icons = icons
        self.setHeaderHidden(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.populate_tree()
        self.expandAll()
        self.clicked.connect(self.handle_item_click)

        self.setStyleSheet("""
            QTreeView { 
                color: #FFF; 
                font-size: 16px; 
            }
            QTreeView::item:hover {
                background-color: #2C2F3F;
                border: #2C2F3F;
            }
            QTreeView::item:selected {
                background-color: #44475A;
                border: 1px solid #44475A;
            }
        """)

    def populate_tree(self):
        def add_item(parent, text, callback):
            item = QStandardItem(text)
            item.setData(lambda: callback(self.owner), Qt.ItemDataRole.UserRole)
            parent.appendRow(item)

        # Parent items with icons
        item_nota   = QStandardItem(self.icons["prioridade"], "Nota de Auditoria")
        item_relatorio   = QStandardItem(self.icons["statistics"], "Relatórios")
        item_mensagem      = QStandardItem(self.icons["mensagem"], "Mensagens")
        item_email      = QStandardItem(self.icons["mail"], "E-mail")
        item_oficio      = QStandardItem(self.icons["doc"], "Ofícios")
        item_webscrapping = QStandardItem(self.icons["magnifying-glass"], "Webscrapping")
        item_api          = QStandardItem(self.icons["api"], "API")

        # Adding child items with their respective callbacks
        add_item(item_nota, "NA - Teste1", show_nota_auditoria_teste1)
        add_item(item_nota, "NA - Teste2", show_nota_auditoria_teste2)
        add_item(item_nota, "NA - Teste3", show_nota_auditoria_teste3)
        add_item(item_nota, "Teste1", show_teste_widget)
        add_item(item_oficio, "Ofício do CCIMAR-20", show_oficio_ccimar20_widget)
        add_item(item_api, "Gerar Notas", show_gerar_notas_widget)
        add_item(item_relatorio, "Consultas do Airflow", show_relatorio_consultas_airflow_widget)
        add_item(item_relatorio, "Relatório SGM", show_relatorio_sgm_widget)
        add_item(item_relatorio, "Relatório CCIMAR-11", show_relatorio_ccimar11_widget)
        add_item(item_relatorio, "Relatório COFAMAR", show_relatorio_cofamar_widget)
        add_item(item_relatorio, "Gerar Nota com Cálculo Total", show_relatorio_calculo_total_widget)
        add_item(item_relatorio, "Notas Monitoradas", show_relatorio_notas_monitoradas_widget)
        add_item(item_relatorio, "AUDCONT - Notas Vencidas", show_relatorio_audcont_widget)
        add_item(item_mensagem, "Teste", show_teste_widget)
        add_item(item_email, "Teste", show_teste_widget)
        add_item(item_webscrapping, "Teste", show_teste_widget)

        # Add parent items to the model
        self.model.appendRow(item_nota)
        self.model.appendRow(item_relatorio)
        self.model.appendRow(item_mensagem)
        self.model.appendRow(item_email)
        self.model.appendRow(item_oficio)
        self.model.appendRow(item_webscrapping)
        self.model.appendRow(item_api)

    def handle_item_click(self, index):
        """Handles item click events and executes the associated callback."""
        item = self.model.itemFromIndex(index)
        if item.hasChildren():
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)
        else:
            callback = item.data(Qt.ItemDataRole.UserRole)
            if callable(callback):
                callback()  # Executes the function, now passing the view instance
