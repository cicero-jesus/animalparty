class Adotante:
    """
    Representa um adotante envolvido no processo de reservas/adoções
    e mantém um histórico de eventos utilizado para geração
    de relatórios.
    Esta classe centraliza informações cadastrais e de elegibilidade
    do adotante, além de registrar eventos do histórico (por exemplo:
    visitas, entrevistas, aprovações, recusas e mudanças de status)
    que são relevantes para o fluxo de adoção/reserva e para relatórios
    gerenciais.
    Atributos principais:
    - id: identificador único do adotante
    - nome, idade: dados pessoais
    - criancasEmCasa: presença ou quantidade de crianças no domicílio
    - moradia, areaUtil: tipo de moradia e área útil disponível
    - experienciaPets: experiência prévia com animais
    - outrosAnimais: presença de outros animais no domicílio
    - ptsCompatib: pontuação de compatibilidade calculada
    - elegivel: indicador se o adotante é elegível para adoção
    """
    def __init__(self, id, nome, idade, criancasEmCasa, moradia, areaUtil, experienciaPets, outrosAnimais):
        self.id = id 
        self.__nome = nome
        self.idade = idade
        self.__criancasEmCasa = criancasEmCasa
        self.moradia = moradia
        self.areaUtil = areaUtil
        self.experienciaPets = experienciaPets
        self.outrosAnimais = outrosAnimais
        self.ptsCompatib =  None
        self.elegivel = None

    @property
    def criancasEmCasa(self):
        return self.__criancasEmCasa
    
    @criancasEmCasa.setter
    def criancasEmCasa(self):
        self.__criancasEmCasa = self.criancasEmCasa
    
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, n):
        if self.__nome == "":
            raise ValueError("Nome não pode ser vazio")
        self.__nome = n

    def criar(self):
        print("Criando adotante...")
        with open("p_adotante.json", "a") as file:
            file.write(f"{self.id},{self.__nome},{self.idade},{self.__criancasEmCasa},{self.moradia},{self.areaUtil},{self.experienciaPets},{self.outrosAnimais},{self.ptsCompatib},{self.elegivel}\n")
    
    def atualizar(self):
        pass

    def excluir(self):
        pass

    def validarElegibilidade(self):
        pass

    def calcularCompatibilidade(self):
        pass

    def reservarAnimal(self):
        pass

    def adotarAnimal(self):
        pass

    def adicionarHistorico(self):
        pass

    def obterHistorico(self):
        pass

