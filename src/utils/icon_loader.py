# config/icon_loader.py
from pathlib import Path
from PyQt6.QtGui import QIcon
from paths import ICONS_DIR
import logging

# Configuração de logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Cache para ícones
_icon_cache = {}

def load_icon(icon_name):
    """Carrega e armazena em cache os ícones como QIcon. Verifica se o arquivo existe antes de carregar."""
    if icon_name not in _icon_cache:
        icon_path = ICONS_DIR / icon_name
        if icon_path.exists():
            _icon_cache[icon_name] = QIcon(str(icon_path))
        else:
            logger.warning(f"Ícone '{icon_name}' não encontrado em {icon_path}")
            _icon_cache[icon_name] = QIcon()  # Retorna um ícone vazio em caso de falha
    return _icon_cache[icon_name]

# Funções específicas para carregar ícones usados frequentemente
def load_icons():
    return {
        "initdataprocessing": load_icon("initdataprocessing.png"),    
        "initdatacollection": load_icon("initdatacollection.png"),    
        "initexploration": load_icon("initexploration.png"),    
        "initreport": load_icon("initreport.png"),    

        "api_azul": load_icon("API_azul.png"),    
        "statistics_azul": load_icon("statistics_azul.png"),
        "pdf_button": load_icon("pdf_button.png"),
        "pdf_button_blue": load_icon("pdf_button_blue.png"),
        "planning": load_icon("planning.png"),
        "info": load_icon("info.png"),
        "360-degrees": load_icon("360-degrees.png"),
        "data-science": load_icon("data-science.png"),

        "brasil": load_icon("brasil.png"),
        "mensagem": load_icon("mensagem.png"),
        "excel": load_icon("excel.png"),

        "api": load_icon("api.png"),
        "api_button": load_icon("api_button.png"),
        "sign": load_icon("sign.png"),
        "init": load_icon("init.png"),
        "init_hover": load_icon("init_hover.png"),
        "contrato": load_icon("contrato.png"),
        "contrato_blue": load_icon("contrato_blue.png"),
        "plan": load_icon("plan.png"),
        "plan_hover": load_icon("plan_hover.png"),
        "contract": load_icon("contract.png"),
        "contract_hover": load_icon("contract_hover.png"),
        "config": load_icon("config.png"),
        "config_hover": load_icon("config_hover.png"),
        "confirm": load_icon("confirm.png"),
        "magnifying-glass": load_icon("magnifying-glass.png"),
        "analysis": load_icon("analysis.png"),
        "data_blue": load_icon("data_blue.png"),
        "data": load_icon("data.png"),
}