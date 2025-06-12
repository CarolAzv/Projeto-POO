import json

class Cliente:
    def __init__(self, id, nome, email, senha, fone):
        self.__id = id
        self.set_nome(nome)
        self.set_email(email)
        self.set_senha(senha)
        self.set_fone(fone)
    def set_id(self, id): self.__id = id
    def set_nome(self, nome):
        if nome == "": raise ValueError("Informe seu nome")
        self.__nome = nome
    def set_email(self, email):
        self.__email = email
    def set_senha(self,s):
        if len(s) < 4 : raise ValueError(f"Senha deve ter no mínimo 8 caracteres")
        self.__senha = s
    def set_fone(self, fone): self.__fone = fone

    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_email(self): return self.__email
    def get_senha(self): return self.__senha
    def get_fone(self): return self.__fone
    def __str__(self):
        return f"{self.__id} - {self.__nome} - {self.__email} - {self.__senha} - {self.__fone}"
    def to_dict(self):
        return {"id": self.__id,"nome": self.__nome,"email": self.__email, "senha": self.__senha, "fone": self.__fone}

    
class Clientes:  # Persistência - Armazena os objetos em um arquivo/banco de dados
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
            with open("clientes.json", "r") as arquivo:
                dados = json.load(arquivo)
                for d in dados:
                    obj = Cliente(d["id"], d["nome"], d["email"],d["senha"], d["fone"])
                    cls.objetos.append(obj)
        except FileNotFoundError:
            pass

    @classmethod
    def salvar(cls):
        with open("clientes.json", "w") as arquivo:
            json.dump([obj.to_dict() for obj in cls.objetos], arquivo)

    @classmethod
    def listar_nome(cls, nome):
        cls.abrir()
        for obj in cls.objetos:
            if obj.get_nome() == nome:
                return obj
        return None

