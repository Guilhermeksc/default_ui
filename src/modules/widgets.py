# modules/widgets.py

# Utilidades
from utils.icon_loader import load_icons

from modules.inicio.view import InicioWidget

from modules.ccimar10_auditoria.view import DataCollectionView
from modules.ccimar10_auditoria.model import DataCollectionModel
from modules.ccimar10_auditoria.controller import DataCollectionController

from modules.ccimar11_planejamento.view import PlanejamentoView
from modules.ccimar11_planejamento.model import PlanejamentoModel
from modules.ccimar11_planejamento.controller import PlanejamentoController

from modules.ccimar12_licitacao.view import CCIMAR12View
from modules.ccimar12_licitacao.model import CCIMAR12Model
from modules.ccimar12_licitacao.controller import CCIMAR12Controller

from modules.module5_ccimar16.view import CCIMAR16View
from modules.module5_ccimar16.model import CCIMAR16Model
from modules.module5_ccimar16.controller import CCIMAR16Controller



__all__ = [
    "InicioWidget",

    "DataCollectionView",
    "DataCollectionModel",
    "DataCollectionController",

    "PlanejamentoView",
    "PlanejamentoModel",
    "PlanejamentoController",

    "CCIMAR12View",
    "CCIMAR12Model",
    "CCIMAR12Controller",

    "CCIMAR16View",
    "CCIMAR16Model",
    "CCIMAR16Controller",
    
    # Utils
    "load_icons"
    ]