class Animal():
    """
    Representa um animal disponível para adoção/reserva no sistema
    e centraliza seu histórico de eventos para relatórios.

    Esta classe gerencia informações cadastrais e de saúde do animal,
    além de registrar eventos do histórico (por exemplo: entrada,
    quarentena, vacinação, reservas, adoções e mudanças
    de status) que são essenciais para rastreabilidade completa
    e geração de relatórios gerenciais.

    O status do animal evoluiciona ao longo do fluxo: recém-chegado,
    em quarentena, disponível para adoção, reservado, adotado ou
    marcado como inadoptável conforme saúde e comportamento.

    Atributos principais:
    - id: identificador único do animal
    - especie, raca: classificação do animal
    - nome, sexo: dados de identificação
    - idadeMeses: idade em meses (permite precisão em filhotes)
    - porte: tamanho do animal (pequeno, médio, grande)
    - temperamento: descrição comportamental para compatibilidade
    - status: estado atual (recém-chegado, quarentena, disponível,
      reservado, adotado, inadoptável)
    - dataEntrada: data de chegada na instituição
    - dataAdocao: data da efetivação da adoção (se aplicável)
    - historicoEventos: registro de todos os eventos do ciclo de vida do animal
    """
    def __init__(self, id, especie, raca, nome, sexo, idadeMeses, porte, temperamento, status, historicoEventos=None, dataEntrada=None, dataAdocao=None):
        self.id = id
        self.especie = especie
        self.raca = raca
        self.nome = nome
        self.sexo = sexo
        self.idadeMeses = idadeMeses
        self.porte = porte
        self.temperamento = temperamento
        self.status = status
        self.historicoEventos = historicoEventos
        self.dataEntrada = dataEntrada
        self.dataAdocao = dataAdocao
        pass

    def criar(self):
        pass

    def atualizar(self):
        pass

    def excluir(self):
        pass

    def registrarEvento(self):
        pass

    def alterarStatus(self):
        pass

    def calcularAdotabilidade(self):
        pass

    def Quarentena(self):
        pass

    def marcarComoInadotavel(self):
        pass

class Cachorro(Animal):
   def __init__(self, id, raca, nome, sexo, idadeMeses, porte, temperamento, status, historicoEventos=None, dataEntrada=None, dataAdocao=None):
        # chamando o construtor da classe pai (Animal)
        super().__init__(id, "Cachorro", raca, nome, sexo, idadeMeses, porte, temperamento, status, historicoEventos, dataEntrada, dataAdocao)
        pass
   
class Gato(Animal):
   def __init__(self, id, raca, nome, sexo, idadeMeses, porte, temperamento, status, historicoEventos=None, dataEntrada=None, dataAdocao=None):
        # chamando o construtor da classe pai (Animal)
        super().__init__(id, "Gato", raca, nome, sexo, idadeMeses, porte, temperamento, status, historicoEventos, dataEntrada, dataAdocao)
        pass