from PyQt6.QtSql import QSqlQuery
import pandas as pd

def insert_execucao_licitacao(database_manager, df):
    """Inserts execution data from a DataFrame into the database."""
    
    if df.empty:
        print("Error: Empty DataFrame. No data to insert.")
        return

    for _, row in df.iterrows():
        cod_siafi = row["COD SIAFI"]

        # Validate and convert COD SIAFI
        if pd.isna(cod_siafi):
            print("Error: COD SIAFI is empty. Skipping insertion...")
            continue

        try:
            cod_siafi = int(float(cod_siafi))  # Ensure it's an integer without .0
        except ValueError:
            print(f"Error converting COD SIAFI ({cod_siafi}) to integer. Skipping...")
            continue

        # Check if the military organization exists
        query = "SELECT cod_siafi FROM organizacoes_militares WHERE cod_siafi = ?"
        result = database_manager.execute_query(query, (cod_siafi,))
        
        if not result:
            print(f"Error: Military Organization not found for SIAFI code {cod_siafi}. Skipping insertion...")
            continue

        # Prepare the insert statement
        insert_query = """
        INSERT INTO criterio_execucao_licitacao (
            cod_siafi, valor_convite, valor_tomada_preco, valor_concorrencia, 
            valor_dispensa, valor_inexigibilidade, valor_nao_se_aplica, 
            valor_suprimento_fundos, valor_regime_diferenciado, valor_cons, 
            valor_pregao_eletronico, valor_credenciamento
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        valores = [
            cod_siafi,
            _parse_float(row["VALOR CONVITE"]),
            _parse_float(row["VALOR TP"]),
            _parse_float(row["VALOR CONC"]),
            _parse_float(row["VALOR DISP LICIT"]),
            _parse_float(row["VALOR INEXIG"]),
            _parse_float(row["VALOR NÃO SE APLICA"]),
            _parse_float(row["VALOR SF"]),
            _parse_float(row["VALOR REG DIF CONT PUB"]),
            _parse_float(row["VALOR CONS"]),
            _parse_float(row["VALOR PREGAO"]),
            _parse_float(row["VALOR CRED"])
        ]

        success = database_manager.execute_update(insert_query, tuple(valores))
        if success:
            print(f"✅ Execution record successfully inserted for OM {cod_siafi}.")
        else:
            print(f"❌ Error inserting execution data for OM {cod_siafi}.")

def _parse_float(value):
    """Converts values to float, handling NaN and empty values."""
    try:
        return float(value) if pd.notna(value) else None
    except ValueError:
        return None
