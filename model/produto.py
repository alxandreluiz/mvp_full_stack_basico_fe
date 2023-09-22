from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base


class Produto(Base):
    __tablename__ = 'produto'

    id = Column("id_produto", Integer, primary_key=True)
    nome = Column(String(140))
    quantidade = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(String(10))

    # Definição do relacionamento entre o produto e o comentário.
    # Essa relação é implicita, não está salva na tabela 'produto',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.    

    def __init__(self, nome:str, quantidade:int, valor:float,
                 data_insercao:str):
        """
        Cria um Produto

        Arguments:
            nomeItem: nome do produto.
            quantidade: quantidade que se espera comprar daquele produto
            valor: valor esperado para o produto
            data_insercao: data de quando o produto foi inserido à base
        """        
        self.nome = nome
        self.quantidade = quantidade
        self.valor = valor
        self.data_insercao = data_insercao    
