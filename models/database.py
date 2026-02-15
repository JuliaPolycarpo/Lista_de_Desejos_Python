from sqlite3 import Connection, connect, Cursor 
import traceback
from types import TracebackType
from typing import Any, Self, Optional, Type
from dotenv import load_dotenv
import os

load_dotenv() #Procura um arquivo .env com variáveis
DB_PATH = os.getenv('DATABASE', './data/desejos.db') #Pega a variável DATABASE do .env, ou usa o caminho padrão se não encontrar

def init_db(db_name: str = DB_PATH) -> None:
    with connect(db_name) as conn:
        conn.execute('''
         CREATE TABLE IF NOT EXISTS desejos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_desejo TEXT NOT NULL,
            tipo_desejo TEXT,
            indicado_por TEXT);
        ''')

class Database:
    """Classe que gerencia conexões e operações com um banco de dados SQLite. Utiliza o protocolo de gerencimento de contexto para garantir que a conexão seja encerrada corretamente."""
    def __init__(self, db_name: str = DB_PATH) -> None:
        self.connection: Connection = connect(db_name)
        self.cursor = self.connection.cursor()
        
    def executar(self, query: str, params: tuple = ()) -> Cursor:
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor
    
    def buscar_tudo(self, query: str, params: tuple = ()) -> list[Any]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self) -> None:
        self.connection.close()

    # Metodo de entrada do contexto
    def __enter__(self) -> Self:
        return self
    
     # Metodo de saida do contexto
    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], tb: Optional[TracebackType]) -> None:

        if exc_type is not None:
            print('Exceção capturada no contexto:')
            print(f'Tipo: {exc_type.__name__}')
            print(f'Mensagem: {exc_value}')
            print ('Traceback completo:')
            traceback.print_tb(tb)
        self.close()

print("BANCO USADO:", DB_PATH)