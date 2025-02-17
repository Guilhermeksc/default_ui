# modules/widgets.py

# Utilidades
from utils.icon_loader import load_icons

from modules.inicio.view import InicioWidget

from modules.module2_pre_processamento.view import PlanejamentoView
from modules.module2_pre_processamento.model import PlanejamentoModel
from modules.module2_pre_processamento.controller import PlanejamentoController

from modules.module5_ccimar16.view import CCIMAR16View
from modules.module5_ccimar16.model import CCIMAR16Model
from modules.module5_ccimar16.controller import CCIMAR16Controller

__all__ = [
    "InicioWidget",

    "PlanejamentoView",
    "PlanejamentoModel",
    "PlanejamentoController",

    "CCIMAR16View",
    "CCIMAR16Model",
    "CCIMAR16Controller",
    
    # Utils
    "load_icons"
    ]