# paths/__init__.py

# Importando diretamente os objetos ou funções de cada módulo interno
from .base_path import *
from .config_path import *
from .planejamento  import *
from .ccimar10_auditoria import *
from .module5_ccimar16 import *

# Definindo __all__ para controle explícito do que será exportado
__all__ = [
    # base_path
    "BASE_DIR", "CONFIG_FILE", "DATABASE_DIR", "MODULES_DIR", "JSON_DIR", "SQL_DIR", 
    "ASSETS_DIR", "TEMPLATE_DIR", "STYLE_PATH", "ICONS_DIR", "ICONS_MENU_DIR", "CONTROLE_DADOS",
    
    # planejamento
    "DATA_PLANEJAMENTO_PATH", "TEMPLATE_PLANEJAMENTO_DIR",
    
    # ccimar10_auditoria
    "DATA_COLLECTION_DIR", "DATA_COLLECTION_PATH",
    
    # module5_ccimar16
    "CCIMAR16_DIR", "DATA_CCIMAR16_PATH", "TEMPLATE_TEST_PATH",

    # config_path
    "PRE_DEFINICOES_JSON", "ORGANIZACOES_FILE", "AGENTES_RESPONSAVEIS_FILE", "PDF_DIR",
    ]
