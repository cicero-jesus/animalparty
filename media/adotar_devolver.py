class Adotar_devolver:
    """
    Classe para gerenciar o processo de adoção e devolução de animais.

    Esta classe atua como um elo entre os animais disponíveis para adoção
    e os adotantes interessados, registrando reservas, efetivações de adoção,
    devoluções e gerenciando contratos e taxas associadas.

    Dados utilizados:
    - Animal: informações cadastrais, status atual e histórico de eventos.
    - Adotante: dados pessoais, elegibilidade e histórico de adoções.
    - Histórico de Adoção/Devolução: registros detalhados de cada transação
      envolvendo adoção e devolução.
    Atributos principais:
    - id: identificador único da transação
    - animalId: referência ao animal adotado
    - adotanteId: referência ao adotante
    - dataReserva: data em que a reserva foi feita
    - dataExpiracaoReserva: data limite para efetivação da adoção
    - dataAdocao: data em que a adoção foi efetivada
    - dataDevolucao: data em que o animal foi devolvido (se aplicável)
    - motivoDevolucao: razão para a devolução (se aplicável)
    - contrato: detalhes do contrato de adoção
    - estrategiaTaxa: política de taxas aplicadas (se houver)
    """
    def __init__(self, id, animalId, adotanteId, dataReserva, dataExpiracaoReserva, dataAdocao, dataDevolucao, motivoDevolucao, contrato, estrategiaTaxa):
        self.id = id
        self.animalId = animalId
        self.adotanteId = adotanteId
        self.dataReserva = dataReserva
        self.dataExpiracaoReserva = dataExpiracaoReserva
        self.dataAdocao = dataAdocao
        self.dataDevolucao = dataDevolucao
        self.motivoDevolucao = motivoDevolucao
        self.__contrato = contrato
        self.estrategiaTaxa = estrategiaTaxa

    @property
    def contrato(self):
        return self.__contrato
    
    @contrato.setter
    def contrato(self, contrato):
        self.__contrato = contrato

    def reservar(self):
        pass

    def expirarReserva(self):
        pass

    def efetivarAdocao(self):
        pass

    def gerarContrato(self):
        pass

    def calcularTaxa(self):
        pass

    def registrarDevolucao(self):
        pass

    def enviarNotProxFila(self):
        pass