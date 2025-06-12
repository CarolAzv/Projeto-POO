from categoria import Categorias
from produto import Produtos
from cliente import Cliente, Clientes
from venda import Venda, Vendas
import json

class UI_visitante:  # Visão/Apresentação - Não tem instância
    carrinho = None   # atributo de classe
    @staticmethod
    def menu():
        print("|------------------------------------------------|")
        print("| Categorias e Produtos                          |")
        print("| 1-Listar Categorias, 2-Listar Produtos         |")
        print("|------------------------------------------------|")
        print("| Cadastro de Clientes                           |")
        print("| 3-Cadastrar, 4-Login                           |")
        print("|------------------------------------------------|")
        print("| 99-FIM                                         |")
        print("|------------------------------------------------|")
        print()
        op = int(input("Selecione uma opção: "))
        print()
        return op

    @staticmethod
    def main(): 
        op = 0
        while op != 99:
            op = UI_visitante.menu()
            if op == 1: UI_visitante.categoria_listar()
            if op == 2: UI_visitante.produto_listar()

            if op == 3: UI_visitante.cliente_inserir()
            if op == 4: UI_visitante.login()
            

    @staticmethod # U - update
# CRUD de Categorias
    def categoria_listar(): 
        for c in Categorias.listar(): print(c)

    # CRUD de Produtos
    @staticmethod # R - read
    def produto_listar(): 
        for c in Produtos.listar(): print(c)

    # CRUD de Clientes
    @staticmethod
    def cliente_inserir(): 
        nome = input("Informe o nome: ")
        email = input("Informe o e-mail: ")
        senha = input("Informe a senha:")
        fone = input("Informe o fone: ")
        from views import View
        View.cliente_inserir(nome, email,senha, fone)

    @staticmethod
    def login():
        email = input("Informe o seu e-mail: ")
        senha = input("Informe a senha: ")

        from views import View
        if email == "admin" and senha == "1234":
            print("Login como ADMIN.")
            UI_visitante.redireciona_admin()
        else:
            cliente = View.autenticar_cliente(email, senha)
            if cliente:
                print(f"Login como CLIENTE: {cliente.get_nome()}")
                UI_visitante.redireciona_cliente(cliente)  # <-- Passa o cliente aqui
            else:
                print("Email ou senha inválidos.")

    @staticmethod
    def redireciona_admin():
        UI.main_admin()
    @staticmethod
    def redireciona_cliente(cliente):
        UI_cliente.main_cliente(cliente)

#-------------------------------------------------CLIENTES-----------------------------------------------------------------------------------------
class UI_cliente:  # Visão/Apresentação - Não tem instância
    carrinho = None   # atributo de classe
    cliente_logado = None
    @staticmethod
    def menu():
        print("|------------------------------------------------|")
        print("| Cadastro de Clientes                           |")
        print("| 1-Atualizar, 2-Logout                          |")
        print("|------------------------------------------------|")
        print("| Categorias e Produtos                          |")
        print("| 3-Listar Categorias, 4-Listar Produtos         |")
        print("|------------------------------------------------|")
        print("| 5-Iniciar um carrinho de compra                |")
        print("| 6-Listar as compras                            |")
        print("| 7-Visualizar carrinho                          |")
        print("| 8-Inserir produto no carrinho                  |")
        print("| 9-Confirmar a compra                           |")
        print("|------------------------------------------------|")
        print("| 99-FIM                                         |")
        print("|------------------------------------------------|")
        print()
        op = int(input("Selecione uma opção: "))
        print()
        return op

    @staticmethod
    def main_cliente(cliente):
        UI_cliente.cliente_logado = cliente
        from views import View 
        View.cadastrar_admin()  
        op = 0
        # clientes = []
        while op != 99:
            op = UI_cliente.menu()
            if op == 1: UI_cliente.cliente_atualizar()
            if op == 2: UI_cliente.logout()

            if op == 3: UI_cliente.categoria_listar()
            if op == 4: UI_cliente.produto_listar()

            if op == 5: UI_cliente.venda_inserir()
            if op == 6: UI_cliente.venda_listar()
            if op == 7: UI_cliente.visualizar_carrinho()
            if op == 8: UI_cliente.inserir_produto_no_carrinho()
            if op == 9: UI_cliente.confirmar_compra()
    # Operações de Venda
    @classmethod
    def venda_inserir(cls): # C - create
        v = Venda(0)
        Vendas.inserir(v)
        cls.carrinho = v
        print("Carrinho pronto para as compras!")
        print("Adicione produtos no carrinho")

    @staticmethod # R - read
    def venda_listar(): 
        for v in Vendas.listar(): 
            print(v)
            for item in VendaItens.listar():
                if item.id_venda == v.get_id():
                    id_produto = item.id_produto
                    descricao = Produtos.listar_id(id_produto).descricao
                    print(f"  {descricao} - Qtd: {item.qtd} - R$ {item.preco:.2f}")


    @classmethod 
    def visualizar_carrinho(cls): 
        if cls.carrinho == None:
            print("Você precisa criar um carrinho primeiro!")
            return
        print("Este é seu carrinho atual: ", cls.carrinho)
        for item in VendaItens.listar():
            if item.id_venda == cls.carrinho.id:
                id_produto = item.id_produto
                descricao = Produtos.listar_id(id_produto).descricao
                print(f"  {descricao} - Qtd: {item.qtd} - R$ {item.preco:.2f}")

    @classmethod 
    def inserir_produto_no_carrinho(cls):
        if cls.carrinho == None:
            print("Você precisa criar um carrinho primeiro!")
            return
        
        # Listar os produtos disponíveis
        UI_cliente.produto_listar()
        id_produto = int(input("Informe o id do produto: "))
        qtd = int(input("Informe a qtd: "))

        # inserir o produto no carrinho
        from views import View
        View.inserir_produto_no_carrinho(cls.carrinho.get_id(), id_produto, qtd)

    @classmethod 
    def confirmar_compra(cls): 
        if cls.carrinho == None:
            print("Você precisa criar um carrinho primeiro!")
            return
        # Na venda (carrinho), colocar o atributo carrinho para False
        cls.carrinho.carrinho = False
        Vendas.atualizar(cls.carrinho)
        # Percorrer os itens da venda (vendaitem-qtd) e baixar o estoque no
        # cadastro de produto (produto-estoque)
        for item in VendaItens.listar():
            if item.id_venda == cls.carrinho.id:
                id_produto = item.id_produto
                qtd = item.qtd
                produto = Produtos.listar_id(id_produto)
                produto.estoque -= qtd
                Produtos.atualizar(produto)

    # CRUD de Clientes
    @staticmethod # U - update
    def cliente_atualizar():
        print("Dados atuais:") 
        print(UI_cliente.cliente_logado)
        print()
        print("Informe os novos dados:")
        nome = input("Nome: ")
        email = input("e-mail: ")
        senha = input("Senha:")
        fone = input("fone: ")        
        #c = Cliente(id, nome, email, fone)
        #Clientes.atualizar(c)
        from views import View
        View.cliente_atualizar(UI_cliente.cliente_logado.get_id(), nome, email,senha, fone)

    # CRUD de Categorias
    def categoria_listar(): 
        for c in Categorias.listar(): print(c)
    @staticmethod # U - update

    # CRUD de Produtos
    @staticmethod # R - read
    def produto_listar(): 
        for c in Produtos.listar(): print(c)

    @staticmethod
    def logout():
        from ui_geral import UI_visitante
        UI_visitante.main()



#---------------------------------------------------ADMIN---------------------------------------------------------------------------------------------------------
#from cliente import Cliente, Clientes
from categoria import Categoria, Categorias
from produto import Produto, Produtos
from venda import Venda, Vendas
from vendaitem import VendaItem, VendaItens

from views import View

class UI:  # Visão/Apresentação - Não tem instância
    carrinho = None   # atributo de classe
    @staticmethod
    def menu_admin():
        print("|------------------------------------------------|")
        print("| Cadastro de Clientes                           |")
        print("| 1-Inserir, 2-Listar, 3-Atualizar, 4-Excluir    |")
        print("|------------------------------------------------|")
        print("| Cadastro de Categorias                         |")
        print("| 5-Inserir, 6-Listar, 7-Atualizar, 8-Excluir    |")
        print("|------------------------------------------------|")
        print("| Cadastro de Produtos                           |")
        print("| 9-Inserir, 10-Listar, 11-Atualizar, 12-Excluir |")
        print("|------------------------------------------------|")
        print("| 13-Iniciar um carrinho de compra               |")
        print("| 14-Listar as compras                           |")
        print("| 15-Visualizar carrinho                         |")
        print("| 16-Inserir produto no carrinho                 |")
        print("| 17-Confirmar a compra                          |")
        print("| 18-Reajuste de preço                           |")
        print("|------------------------------------------------|")
        print("| 19-logout                                      |")
        print("|------------------------------------------------|")
        print("| 99-FIM                                         |")
        print("|------------------------------------------------|")
        print()
        op = int(input("Selecione uma opção: "))
        print()
        return op

    @staticmethod
    def main_admin(): 
        View.cadastrar_admin()  
        op = 0
        # clientes = []
        while op != 99:
            op = UI.menu_admin()
            if op == 1: UI.cliente_inserir() 
            if op == 2: UI.cliente_listar()
            if op == 3: UI.cliente_atualizar()
            if op == 4: UI.cliente_excluir()

            if op == 5: UI.categoria_inserir() 
            if op == 6: UI.categoria_listar()
            if op == 7: UI.categoria_atualizar()
            if op == 8: UI.categoria_excluir()

            if op == 9: UI.produto_inserir() 
            if op == 10: UI.produto_listar()
            if op == 11: UI.produto_atualizar()
            if op == 12: UI.produto_excluir()

            if op == 13: UI_cliente.venda_inserir()
            if op == 14: UI_cliente.venda_listar()
            if op == 15: UI_cliente.visualizar_carrinho()
            if op == 16: UI_cliente.inserir_produto_no_carrinho()
            if op == 17: UI_cliente.confirmar_compra()
            if op == 18: UI.reajuste_preço()
            if op == 19: UI.logout()


    # Operações de Venda
    @classmethod
    def venda_inserir(cls): # C - create
        v = Venda(0)
        Vendas.inserir(v)
        cls.carrinho = v

    @staticmethod # R - read
    def venda_listar(): 
        for v in Vendas.listar(): 
            print(v)
            for item in VendaItens.listar():
                if item.id_venda == v.id:
                    id_produto = item.id_produto
                    descricao = Produtos.listar_id(id_produto).descricao
                    print(f"  {descricao} - Qtd: {item.qtd} - R$ {item.preco:.2f}")


    @classmethod 
    def visualizar_carrinho(cls): 
        if cls.carrinho == None:
            print("Você precisa criar um carrinho primeiro!")
            return
        print("Este é seu carrinho atual: ", cls.carrinho)
        for item in VendaItens.listar():
            if item.id_venda == cls.carrinho.id:
                id_produto = item.id_produto
                descricao = Produtos.listar_id(id_produto).descricao
                print(f"  {descricao} - Qtd: {item.qtd} - R$ {item.preco:.2f}")
    @staticmethod
    def inserir_produto_no_carrinho(cls):
        if cls.carrinho == None:
            print("Você precisa criar um carrinho primeiro!")
            return
        
        # Listar os produtos disponíveis
        UI_cliente.produto_listar()
        id_produto = int(input("Informe o id do produto: "))
        qtd = int(input("Informe a qtd: "))

        # inserir o produto no carrinho
        from views import View
        View.inserir_produto_no_carrinho(cls.carrinho.get_id(), id_produto, qtd)

    @classmethod 
   
    def confirmar_compra(cls): 
        if cls.carrinho == None:
            print("Você precisa criar um carrinho primeiro!")
            return

        print("Formas de pagamento:")
        print("|1- Dinheiro         |")
        print("|2- Cartão de Crédito|")
        print("|3- Cartão de Débito |")
        print("|4- Pix              |")
        op = int(input("Escolha a forma de pagamento: "))
    
        forma = ""
        if op == 1: forma = "Dinheiro"
        elif op == 2: forma = "Cartão de Crédito"
        elif op == 3: forma = "Cartão de Débito"
        elif op == 4: forma = "Pix"
        else:
            print("Compra não pode ser efetuada sem a escolha da forma de pagamento")
            return

        cls.carrinho.forma_pagamento = forma 
        cls.carrinho.carrinho = False
        Vendas.atualizar(cls.carrinho)

        for item in VendaItens.listar():
            if item.id_venda == cls.carrinho.id:
                id_produto = item.id_produto
                qtd = item.qtd
                produto = Produtos.listar_id(id_produto)
                produto.estoque -= qtd
                Produtos.atualizar(produto)

        print(f"Compra confirmada com pagamento via {forma}.")

    # CRUD de Clientes
    @staticmethod
    def cliente_inserir(): # C - create
        # id = int(input("Informe o id do cliente: "))
        nome = input("Informe o nome: ")
        email = input("Informe o e-mail: ")
        fone = input("Informe o fone: ")
        #c = Cliente(0, nome, email, fone)
        #Clientes.inserir(c)
        View.cliente_inserir(nome, email, fone)
    @staticmethod # R - read
    def cliente_listar(): 
        #for c in Clientes.listar(): print(c)
        for c in View.cliente_listar(): print(c)
    @staticmethod # U - update
    def cliente_atualizar(): 
        UI.cliente_listar()
        id = int(input("Informe o id do cliente a ser atualizado: "))
        nome = input("Informe o novo nome: ")
        email = input("Informe o novo e-mail: ")
        fone = input("Informe o novo fone: ")        
        #c = Cliente(id, nome, email, fone)
        #Clientes.atualizar(c)
        View.cliente_atualizar(id, nome, email, fone)
    @staticmethod # D - delete
    def cliente_excluir(): 
        UI.cliente_listar()
        id = int(input("Informe o id do cliente a ser excluído: "))
        #c = Cliente(id, "", "", "")
        #Clientes.excluir(c)
        View.cliente_excluir(id)

    # CRUD de Categorias
    @staticmethod
    def categoria_inserir(): # C - create
        descricao = input("Informe a descrição: ")
        c = Categoria(0, descricao)
        Categorias.inserir(c)
    @staticmethod # R - read
    def categoria_listar(): 
        for c in Categorias.listar(): print(c)
    @staticmethod # U - update
    def categoria_atualizar(): 
        UI.categoria_listar()
        id = int(input("Informe o id da categoria a ser atualizada: "))
        descricao = input("Informe a nova descrição: ")
        c = Categoria(id, descricao)
        Categorias.atualizar(c)
    @staticmethod # D - delete
    def categoria_excluir(): 
        UI.categoria_listar()
        id = int(input("Informe o id da categoria a ser excluída: "))
        c = Categoria(id, "")
        Categorias.excluir(c)

    # CRUD de Produtos
    @staticmethod
    def produto_inserir(): # C - create
        descricao = input("Informe a descrição: ")
        preco = float(input("Informe o preço: "))
        estoque = int(input("Informe o estoque: "))
        UI.categoria_listar()
        id_categoria = int(input("Informe o id da categoria: "))
        c = Produto(0, descricao, preco, estoque)
        c.id_categoria = id_categoria
        Produtos.inserir(c)
    @staticmethod # R - read
    def produto_listar(): 
        for c in Produtos.listar(): print(c)
    @staticmethod # U - update
    def produto_atualizar(): 
        UI.produto_listar()
        id = int(input("Informe o id do produto a ser atualizado: "))
        descricao = input("Informe a nova descrição: ")
        preco = float(input("Informe o novo preço: "))
        estoque = int(input("Informe o novo estoque: "))
        UI.categoria_listar()
        id_categoria = int(input("Informe o id da nova categoria: "))
        c = Produto(id, descricao, preco, estoque)
        c.id_categoria = id_categoria
        Produtos.atualizar(c)
    @staticmethod # D - delete
    def produto_excluir(): 
        UI.produto_listar()
        id = int(input("Informe o id do produto a ser excluído: "))
        c = Produto(id, "", "", "")
        Produtos.excluir(c)
    @classmethod
    def reajuste_preço(cls):
        UI.produto_listar()
        id_produto = int(input("Informe o ID do produto que deseja reajustar: "))
        tipo = input("Informe se o reajuste: 1-Aumento, 2-Desconto:")
        porcentagem = int(input("Informe a porcentagem do reajuste:"))
        if tipo == "1":
            VendaItens.reajuste_precinho(porcentagem,id_produto)
        else:
            VendaItens.reajuste_precinho(porcentagem * -1,id_produto)
        

    @staticmethod
    def logout():
        from ui_geral import UI_visitante
        UI_visitante.main()


        