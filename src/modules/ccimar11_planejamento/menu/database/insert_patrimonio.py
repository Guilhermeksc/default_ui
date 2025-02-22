import pandas as pd

def insert_patrimonio(database_manager, df_data):
    """Inserts patrimony data from two sheets into the database."""

    df_moveis = df_data.get("BENS MOVEIS")
    df_imoveis = df_data.get("BENS IMOVEIS")

    if df_moveis is None or df_imoveis is None:
        print("Error: One or both DataFrames are missing. Skipping insertion.")
        return

    for (_, row_moveis), (_, row_imoveis) in zip(df_moveis.iterrows(), df_imoveis.iterrows()):
        cod_siafi = row_moveis["COD SIAFI"]

        if pd.isna(cod_siafi):
            print("Error: COD SIAFI is empty. Skipping insertion...")
            continue

        try:
            cod_siafi = int(float(cod_siafi))
        except ValueError:
            print(f"Error converting COD SIAFI ({cod_siafi}) to integer. Skipping...")
            continue

        # Validate existence of organization
        query = "SELECT cod_siafi FROM organizacoes_militares WHERE cod_siafi = ?"
        result = database_manager.execute_query(query, (cod_siafi,))
        if not result:
            print(f"Error: Organization not found for SIAFI code {cod_siafi}. Skipping insertion...")
            continue

        # Prepare Insert Query
        insert_query = """
        INSERT INTO criterio_patrimonio (
            cod_siafi,
            total_geral_bens_moveis,
            importacoes_em_andamento_bens_moveis,
            total_geral_bens_imoveis,
            importacoes_em_andamento_bens_imoveis,
            bens_imoveis_a_classificar
        ) VALUES (?, ?, ?, ?, ?, ?)
        """

        valores = [
            cod_siafi,
            _parse_float(row_moveis.get("TOTAL GERAL", 0)),  # Handle missing keys safely
            _parse_float(row_moveis.get("IMPORTACOES EM ANDAMENTO - BENS MOVEIS", 0)),
            _parse_float(row_imoveis.get("TOTAL GERAL", 0)),  # Now from BENS IMOVEIS
            _parse_float(row_imoveis.get("'= OBRAS EM ANDAMENTO", 0)),
            _parse_float(row_imoveis.get("'= BENS IMOVEIS A CLASSIFICAR/ A REGISTRAR", 0)),
        ]

        success = database_manager.execute_update(insert_query, tuple(valores))
        if success:
            print(f"✅ Patrimony data inserted for OM {cod_siafi}.")
        else:
            print(f"❌ Error inserting patrimony data for OM {cod_siafi}.")


def _parse_float(value):
    """Converts values to float, handling NaN and empty values."""
    try:
        return float(value) if pd.notna(value) else None
    except ValueError:
        return None
