import json
from datetime import datetime

class Venda:
    def __init__(self, id):
        self.__id = id       
        self.__data = datetime.now()
        self.__carrinho = True
        self.__total = 0
        self.__id_cliente = 0
        self.__forma_pagamento = None
        self.__carrinho = True
    def set_id(self,id):
        self.__id = id
    def set_data(self,d):
        self.__data = d
    def set_total(self,t):
        self.__total = t
    def set_idCliente(self,id):
        self.__id_cliente = id
    def set_formaPagamento(self,f):
        self.__forma_pagamento = f
    def set_carrinho(self,b):
        self.__carrinho = b
    def get_id(self):
        return self.__id
    def get_data(self):
        return self.__data
    def get_total(self):
        return self.__total
    def get_idCliente(self):
        return self.__id_cliente
    def get_formapagamento(self):
        return self.__forma_pagamento
    def get_carrinho(self):
        return self.__carrinho
    
    def __str__(self):
        return f"{self.get_id()} - {self.get_data().strftime('%d/%m/%Y %H:%M')} - R$ {self.get_total():.2f}"

    def to_json(self):
        dic = {}
        dic["id"] = self.get_id()     
        dic["data"] = self.get_data().strftime("%d/%m/%Y %H:%M:%S")
        dic["carrinho"] = self.get_carrinho()
        dic["total"] = self.get_total()
        dic["id_cliente"] = self.get_idCliente()
        dic["Forma_Pagamento"] = self.get_formapagamento()
        return dic
    
class Vendas:      # Persistência - Armazena os objetos em um arquivo/banco de dados
    objetos = []   # atributo de classe / estático - Não tem instância
    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        m = 0
        for x in cls.objetos:
            if x.get_id() > m: m = x.get_id()
        obj.set_id(m + 1 )  
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
            if obj.get_id() == id: return obj
        return None               
    @classmethod
    def atualizar(cls, obj):
        x = cls.listar_id(obj.get_id())
        if x != None: 
            cls.objetos.remove(x)
            cls.objetos.append(obj)
            cls.salvar()
    @classmethod
    def excluir(cls, obj):
        x = cls.listar_id(obj.get_id())
        if x != None: 
            cls.objetos.remove(x)
            cls.salvar()
    @classmethod


    def abrir(cls):
        cls.objetos = []
        try:
            with open("vendas.json", mode="r") as arquivo:
                s = json.load(arquivo)
                for dic in s:
                    obj = Venda(dic["id"])
                    obj.set_data(datetime.strptime(dic["data"], "%d/%m/%Y %H:%M:%S"))  # com segundos
                    obj.set_carrinho(dic["carrinho"])
                    obj.set_total(dic["total"])
                    obj.set_idCliente(dic["id_cliente"])
                    obj.set_formaPagamento(dic.get("forma_pagamento"))  # pode estar None
                    cls.objetos.append(obj)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass         
    @classmethod
    def salvar(cls):
        with open("vendas.json", mode="w") as arquivo:
            json.dump(cls.objetos, arquivo, default = Venda.to_json)

