import json

class Produto:
    def __init__(self, id, descricao, preco, estoque):
        self.__id = id
        self.set_descricao(descricao)
        self.set_preco(preco)
        self.set_estoque(estoque)
        self.__id_categoria = 0
    def set_id(self,id):
        self.__id = id
    def set_descricao(self,d):
        if d == "": raise ValueError(f"Informe a descrição")
        self.__descricao = d
    def set_preco(self,p):
        if p == 0.0: raise ValueError(f"Informe o preco")
        self.__preco = p
    def set_estoque(self,e):
        if e <= 0: raise ValueError(f"Informe o estoque")
        self.__estoque = e
    def set_idCategoria(self,id):
        self.__id_categoria = id
    def get_id(self):
        return self.__id
    def get_descricao(self):
        return self.__descricao
    def get_preco(self):
        return self.__preco
    def get_estoque(self):
        return self.__estoque
    def __str__(self):
        return f"{self.__id} - {self.__descricao} - R$ {self.__preco:.2f} - estoque: {self.__estoque}"
    def to_dict(self):
        return {"id": self.__id,"descricao": self.__descricao,"preco": self.__preco,"estoque": self.__estoque,"id_categoria": self.__id_categoria}

class Produtos:  # Persistência - Armazena os objetos em um arquivo/banco de dados
    objetos = [] # atributo de classe / estático - Não tem instância


    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        m = max((x.get_id() for x in cls.objetos), default=0)
        obj.set_id(m + 1)
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
            if obj.get_id() == id:
                return obj
        return None

    @classmethod
    def atualizar(cls, obj):
        x = cls.listar_id(obj.get_id())
        if x:
            cls.objetos.remove(x)
            cls.objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        x = cls.listar_id(obj.get_id())
        if x:
            cls.objetos.remove(x)
            cls.salvar()

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("produtos.json", mode="r") as arquivo:
                dados = json.load(arquivo)
                for d in dados:
                    obj = Produto(d["id"], d["descricao"], d["preco"], d["estoque"])
                    obj.set_idCategoria(d["id_categoria"])
                    cls.objetos.append(obj)
        except FileNotFoundError:
            pass

    @classmethod
    def salvar(cls):
        with open("produtos.json", mode="w") as arquivo:
            json.dump([obj.to_dict() for obj in cls.objetos], arquivo)




