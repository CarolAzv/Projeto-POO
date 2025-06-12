import json

class Categoria:
    def __init__(self, id, descricao):
        self.__id = id
        self.set_descricao(descricao)
    def set_id(self, id):
        self.__id = id
    def set_descricao(self, descricao):
        if descricao == "":
            raise ValueError("Informe a descrição")
        self.__descricao = descricao
    def get_id(self):
        return self.__id
    def get_descricao(self):
        return self.__descricao
    def to_dict(self):
        return {"id": self.__id, "descricao": self.__descricao}
    def __str__(self):
        return f"{self.__id} - {self.__descricao}"

class Categorias: # Persistência - Armazena os objetos em um arquivo/banco de dados
    objetos = []  # atributo de classe / estático - Não tem instância

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        m = 0
        for x in cls.objetos:
            if x.get_id() > m: m = x.get_id()
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
            with open("categorias.json", mode="r") as arquivo:
                s = json.load(arquivo)
                for dic in s:
                    obj = Categoria(dic["id"], dic["descricao"])
                    cls.objetos.append(obj)
        except FileNotFoundError:
            pass
    @classmethod
    def salvar(cls):
        with open("categorias.json", mode="w") as arquivo:
            json.dump([obj.to_dict() for obj in cls.objetos], arquivo) # to_dict() vai salvar o obj como dicionario no arquivo
