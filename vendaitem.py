import json

class VendaItem:
    def __init__(self, id, qtd, preco):
        self.__id = id       
        self.__qtd = qtd
        self.__preco = preco
        self.__id_venda = 0
        self.__id_produto = 0
    def set_id(self, id):
        self.__id = id
    def set_qtd(self, qtd):
        if qtd == 0.0: raise ValueError(f"Informe a quantidade")
        self.__qtd = qtd
    def set_preco(self, preco):
        if preco == 0.0: raise ValueError(f"Informe o preco")
        self.__preco = preco
    def set_id_venda(self, id_venda):
        self.__id_venda = id_venda
    def set_id_produto(self, id_produto):
        self.__id_produto = id_produto
    def get_id(self):
        return self.__id
    def get_qtd(self):
        return self.__qtd
    def get_preco(self):
        return self.__preco
    def get_id_venda(self):
        return self.__id_venda
    def get_id_produto(self):
        return self.__id_produto
    def __str__(self):
        return f"{self.__id} - {self.__qtd} - R$ {self.__preco:.2f}"

class VendaItens:    # Persistência - Armazena os objetos em um arquivo/banco de dados
    objetos = []     # atributo de classe / estático - Não tem instância
    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        m = 0
        for x in cls.objetos:
            if x.id > m: m = x.id
        obj.id = m + 1    
        cls.objetos.append(obj)
        cls.salvar() 
    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.objetos
    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for obj in cls.objetos:
            if obj.id == id: return obj
        return None               
    @classmethod
    def atualizar(cls, obj):
        x = cls.listar_id(obj.id)
        if x != None: 
            cls.objetos.remove(x)
            cls.objetos.append(obj)
            cls.salvar()
    @classmethod
    def excluir(cls, obj):
        x = cls.listar_id(obj.id)
        if x != None: 
            cls.objetos.remove(x)
            cls.salvar()
    @classmethod
    def abrir(cls):
        cls.objetos = [] 
        try:   
            with open("vendaitens.json", mode="r") as arquivo:
                s = json.load(arquivo)
                for dic in s: 
                    obj = VendaItem(dic["id"], dic["qtd"], dic["preco"])
                    obj.id_venda = dic["id_venda"]
                    obj.id_produto = dic["id_produto"]
                    cls.objetos.append(obj)
        except FileNotFoundError:
            pass            
    @classmethod
    def salvar(cls):
        with open("vendaitens.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default = vars)
    @classmethod
    def reajuste_precinho(cls, porcentagem, id_produto):
        from produto import Produtos
        produto = Produtos.listar_id(id_produto)

        if produto is None:
            print("Produto não encontrado.")
            return

        preco_atual = produto.get_preco()
        novo_preco = preco_atual * (1 + (porcentagem / 100))

        produto.set_preco(novo_preco)
        Produtos.atualizar(produto)

        print(f"Produto {produto.get_descricao()} atualizado: R$ {preco_atual:.2f} → R$ {novo_preco:.2f}")

                


        
