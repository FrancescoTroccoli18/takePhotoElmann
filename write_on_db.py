import pyodbc
import os
import json
import datetime
import streamlit as st
from datetime import datetime
import pandas as pd
from typing import List, Dict, Optional
from const import *

#SQLSERVERDB
DB_CONFIG = {
    #"server": "TEC37315\\SQLEXPRESS", #FRANCESCO
    #"server": "TEC28684\\SQLEXPRESS", #FEDERICO
    #"database": "Elmann",
    "schema": "dbo",
    "driver": "{SQL Server}"
}

def get_connection():
    server = SQL_SERVER_DB_SERVER.strip().replace('\\\\', '\\')
    database = SQL_SERVER_DB_NAME.strip()
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"TRUSTED_CONNECTION=YES;"
    )
    return pyodbc.connect(conn_str)

# QUERIES
# Scrittura su DB
def insert_photo(token, codice_test, image, ut_ins):
    """
    Inserisce una nuova riga nella tabella dbo.app_photo.
    I campi ID e Dt_Ins vengono gestiti automaticamente da SQL Server.
    """
    query = """
        INSERT INTO dbo.app_photo
            (Token, Codice_Test, Image, Ut_Ins)
        VALUES (?, ?, ?, ?)
    """

    values = (token, codice_test, image, ut_ins)

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
    except Exception as e:
        raise RuntimeError(f"Errore durante l'inserimento in 'dbo.app_photo': {e}") from e