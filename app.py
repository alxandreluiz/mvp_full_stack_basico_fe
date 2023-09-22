from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Produto
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de produtos à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/cadastrar_produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """

    produto = Produto(
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor,
        data_insercao=form.data_insercao)
    logger.warning(f"Adicionando produto de nome: '{produto.nome}'")
    try:        
        session = Session()        
        session.add(produto)                
        session.commit()
        logger.debug(f"Adicionado produto de nome: '{produto.nome}'")
        return apresenta_produto(produto), 200    

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível adicionar o novo item "
        logger.warning(f"Erro ao adicionar produto '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/buscar_produtos', tags=[produto_tag],
         responses={"200": ListagemVendasProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    logger.debug(f"Coletando produtos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(Produto).all()        

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos), 200


@app.get('/buscar_produtos_por_nome', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por um Produto a partir do nome do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_nome = query.nome
    logger.debug(f"Coletando dados sobre produto #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.nome == produto_nome).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não adicionado"
        logger.warning(f"Erro ao buscar produto '{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Produto econtrado: '{produto.nome}'")
        # retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/deletar_produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do nome de produto informado

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Deletando dados sobre produto #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{produto_nome}")
        return {"mesage": "Produto removido", "nome": produto_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não adicionado."
        logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404

