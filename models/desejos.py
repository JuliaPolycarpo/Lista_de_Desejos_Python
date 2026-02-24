from sqlite3 import Cursor
from models.database import Database
from typing import Self, Any, Optional



class Desejo:
    """Classe que representa um desejo (filme, série, jogo, livro, etc.)
    com métodos para salvar, obter, excluir e atualizar dados no banco."""

    def __init__(self: Self, titulo_desejo: Optional[str], tipo_desejo: Optional[str] = None, indicado_por: Optional[str] = None, imagem: Optional[str] = None,  id_desejo: Optional[int] = None) -> None:
        self.titulo_desejo = titulo_desejo
        self.tipo_desejo = tipo_desejo
        self.indicado_por = indicado_por
        self.imagem = imagem
        self.id_desejo = id_desejo

    @classmethod
    def id(cls, id: int) -> Optional[Self]:
        with Database() as db:
            query: str = 'SELECT titulo_desejo, tipo_desejo, indicado_por, imagem FROM desejos WHERE id = ?;'
            params: tuple = (id,)
            resultado: list[Any] = db.buscar_tudo(query, params)

           #Para parar de dar erro no desempacotamento ([[titulo, tipo]] = resultado), fiz isso aqui:
            if not resultado:
                return None
            
            titulo, tipo, indicado_por, imagem = resultado[0] #precisa disso para desempacotar a lista de resultados que é uma tupla (titulo, tipo, indicado_por, imagem)
        return cls(titulo_desejo=titulo, tipo_desejo=tipo, indicado_por=indicado_por, imagem=imagem, id_desejo=id)

    def salvar_desejo(self: Self) -> None:
        with Database() as db:
            query: str = 'INSERT INTO desejos (titulo_desejo, tipo_desejo, indicado_por, imagem) VALUES (?, ?, ?, ?);'
            params: tuple = (self.titulo_desejo, self.tipo_desejo, self.indicado_por, self.imagem)
            db.executar(query, params)

    @classmethod
    def obter_desejos(cls) -> list[Self]:
        with Database() as db:
            query: str = 'SELECT titulo_desejo, tipo_desejo, indicado_por, imagem, id FROM desejos;'
            resultados: list[Any] = db.buscar_tudo(query)
            desejos: list[Self] = [cls(titulo, tipo, indicado_por, imagem, id) for titulo, tipo, indicado_por, imagem, id in resultados]
            return desejos

    def excluir_desejo(self: Self) -> Cursor:
        with Database() as db:
            query: str = 'DELETE FROM desejos WHERE id = ?;'
            params: tuple = (self.id_desejo,)
            resultado: Cursor = db.executar(query, params)
            return resultado

    def atualizar_desejo(self: Self) -> Cursor:
        with Database() as db:  
            query: str = 'UPDATE desejos SET titulo_desejo = ?, tipo_desejo = ?, indicado_por = ?, imagem = ? WHERE id = ?;'       
            params: tuple = (self.titulo_desejo, self.tipo_desejo, self.indicado_por, self.imagem, self.id_desejo)
            resultado: Cursor = db.executar(query, params)
            return resultado


