# src/modules/ccimar11_planejamento/menu/treeview_menu.py

from PyQt6.QtWidgets import QTreeView, QAbstractItemView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from .menu_callbacks import (  
    show_criterio1_execucao_licitacao, show_criterio2_pagamento,
    show_criterio3_munic, show_criteriox_omps, show_criterio4_patrimonio,
    show_oficio_ccimar20_widget, show_gerar_notas_widget
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
        item_paint   = QStandardItem(self.icons["analytics"], "PAINT")
        item_relatorio   = QStandardItem(self.icons["report"], "RAINT")
        item_monitoramento   = QStandardItem(self.icons["statistics"], "Monitoramento")

        # Adding child items with their respective callbacks
        add_item(item_paint, "Execução/Licitação", show_criterio1_execucao_licitacao)
        add_item(item_paint, "Pagamento", show_criterio2_pagamento)
        add_item(item_paint, "Municiamento", show_criterio3_munic)
        add_item(item_paint, "Patrimônio", show_criterio4_patrimonio)
        add_item(item_paint, "Última Auditoria", show_criterio3_munic)
        add_item(item_paint, "Notas de Auditoria", show_criterio3_munic)
        add_item(item_paint, "Foco Externo", show_criterio3_munic)
        add_item(item_paint, "OC", show_criterio3_munic)
        add_item(item_paint, "OMPS", show_criteriox_omps)
        add_item(item_monitoramento, "Patrimônio", show_oficio_ccimar20_widget)
        add_item(item_monitoramento, "Anos", show_gerar_notas_widget)

        # Add parent items to the model
        self.model.appendRow(item_paint)
        self.model.appendRow(item_relatorio)
        self.model.appendRow(item_monitoramento)


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
