class Adotante:
    """
    Classe responsável por...
    """
    def __init__(self, id, nome, idade, criancasEmCasa):
        self.id = id 
        self.nome = nome
        self.idade = idade
        self.__criancasEmCasa = criancasEmCasa
        pass

    @property
    def criancasEmCasa(self):
        return f"{self.__criancasEmCasa}"
    
    @criancasEmCasa.setter
    def criancasEmCasa(self):
        self.__criancasEmCasa = criancasEmCasa
    
    def exibir(self):
        return f"Ola {self.nome}, vc tem {self.criancasEmCasa}"
