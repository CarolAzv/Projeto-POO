from cliente import Cliente, Clientes
from categoria import Categoria, Categorias
from produto import Produto, Produtos
from venda import Venda, Vendas
from vendaitem import VendaItem, VendaItens

class View:
    def cadastrar_admin():
        for cliente in Clientes.listar():
            if cliente.get_email() == "admin" : return
        View.cliente_inserir("admin", "admin","1234", "12344567")        
    def cliente_inserir(nome, email,senha, fone):
        c = Cliente(0, nome, email,senha, fone)
        Clientes.inserir(c)
    def cliente_listar():
       return Clientes.listar()
    def cliente_atualizar(id, nome, email,senha, fone):
        c = Cliente(id, nome, email,senha, fone)
        Clientes.atualizar(c)
    def cliente_excluir(id):
        c = Cliente(id, "", "", "")
        Clientes.excluir(c)
    @staticmethod
    def autenticar_cliente(email, senha):
        for cliente in Clientes.listar():
            if cliente.get_email() == email and cliente.get_senha() == senha:
                return cliente  
        return None  

    #================================================adição================================================
    @staticmethod
    def inserir_produto_no_carrinho(id_carrinho, id_produto, qtd):
         # Consultar preço do produto
        product = Produtos.listar_id(id_produto)
        preco = product.get_preco()
        # Instanciar o item da venda
        vi = VendaItem(0, qtd, preco)
        vi.set_id_venda(carrinho.get_id()) 
        vi.set_id_produto( id_produto)
        # Inserir o item da venda
        VendaItens.inserir(vi)
        carrinho = Vendas.listar_id(id_carrinho)
        # Atualizar o total da venda (carrinho)
        subtotal = qtd * preco
        carrinho.set_total(subtotal) 
        Vendas.atualizar(carrinho)