from PyQt6.QtSql import QSqlQuery
import pandas as pd

def insert_munic(db, cod_siafi, uasg, codigo_om, sigla_om, nome_om, despesa_autorizada, quantidade_de_notas, uf, area_om, ultima_auditoria):
    """Inserts a new record into the criterio_munic table."""
    query = QSqlQuery(db)

    query.prepare("SELECT id_om FROM organizacoes_militares WHERE cod_siafi = ?")
    query.addBindValue(cod_siafi)
    if not query.exec() or not query.next():
        print(f"Error: Military Organization not found for SIAFI code {cod_siafi}")
        return

    id_om = query.value(0)

    sql = """
    INSERT INTO criterio_munic (
        id_om, uasg, codigo_om, sigla_om, nome_om, despesa_autorizada, quantidade_de_notas, uf, area_om, ultima_auditoria
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    query.prepare(sql)
    query.addBindValue(id_om)
    query.addBindValue(uasg)
    query.addBindValue(codigo_om)
    query.addBindValue(sigla_om)
    query.addBindValue(nome_om)
    query.addBindValue(despesa_autorizada)
    query.addBindValue(quantidade_de_notas)
    query.addBindValue(uf)
    query.addBindValue(area_om)
    query.addBindValue(ultima_auditoria)

    if not query.exec():
        print("Error inserting into criterio_munic:", query.lastError().text())
    else:
        print(f"Record successfully inserted into criterio_munic for OM {nome_om}.")