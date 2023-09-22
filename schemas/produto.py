from pydantic import BaseModel
from typing import Optional, List
from model.produto import Produto

class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "Camisa"
    quantidade: Optional[int] = 25
    valor: float = 10.00  
    data_insercao: str = "dd/mm/aaaa" 

class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = "Teste"


class ListagemVendasProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos:List[ProdutoSchema]


def apresenta_produtos(produtos: List[Produto]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for produto in produtos:
        result.append({
            "id": produto.id,
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "valor": produto.valor,
            "data": produto.data_insercao,
        })

    return {"produtos": result}


class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto + comentários.
    """
    id: int = 1
    nome: str = "Camisa Vermelha"
    quantidade: Optional[int] = 12
    valor: float = 12.50    

class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_produto(produto: Produto):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": produto.id,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "valor": produto.valor,
        "data": produto.data_insercao,
    }
