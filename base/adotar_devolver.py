from datetime import datetime, timedelta
import uuid

class adotarDevolver:
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
    """

    def __init__(self, estrategiaTaxa=None):
        self.estrategiaTaxa = estrategiaTaxa

    def reservar(self, adotante, animal, dias_reserva=3):
        if animal.status != "disponível":
            raise ValueError(f"Animal {animal.id} não está disponível para reserva.")

        if not adotante.elegivel:
            raise ValueError(f"Adotante {adotante.id} não é elegível para reservar.")

        data_reserva = datetime.now()
        data_exp = data_reserva + timedelta(days=dias_reserva)

        # Atualiza animal
        animal.alterarStatus("reservado")
        animal.registrarEvento("reserva", {
            "adotanteId": adotante.id,
            "data": data_reserva.isoformat()
        })

        # Atualiza adotante
        adotante.adicionarHistorico({
            "evento": "reserva",
            "animalId": animal.id,
            "data": data_reserva.isoformat()
        })

        # Gera transação
        transacao = {
            "id": str(uuid.uuid4()),
            "animalId": animal.id,
            "adotanteId": adotante.id,
            "dataReserva": data_reserva.isoformat(),
            "dataExpiracaoReserva": data_exp.isoformat(),
            "dataAdocao": None,
            "dataDevolucao": None,
            "motivoDevolucao": None,
            "contrato": None
        }

        return transacao

    def expirarReserva(self, transacao, animal, adotante):
        if animal.status != "reservado":
            return  # nada a fazer

        data_exp = datetime.fromisoformat(transacao["dataExpiracaoReserva"])
        if datetime.now() < data_exp:
            return  # ainda não expirou

        animal.alterarStatus("disponível")
        animal.registrarEvento("reserva expirada", {"data": datetime.now().isoformat()})

        adotante.adicionarHistorico({
            "evento": "reserva expirada",
            "animalId": animal.id,
            "data": datetime.now().isoformat()
        })

    def efetivarAdocao(self, transacao, animal, adotante):
        if animal.status != "reservado":
            raise ValueError("Animal não está reservado.")

        data_adocao = datetime.now()

        # Atualiza animal
        animal.alterarStatus("adotado")
        animal.dataAdocao = data_adocao
        animal.registrarEvento("adoção efetivada", {
            "adotanteId": adotante.id,
            "data": data_adocao.isoformat()
        })

        # Atualiza adotante
        adotante.adicionarHistorico({
            "evento": "adoção efetivada",
            "animalId": animal.id,
            "data": data_adocao.isoformat()
        })

        # Gera contrato
        transacao["contrato"] = self.gerarContrato(transacao, animal, adotante)
        transacao["dataAdocao"] = data_adocao.isoformat()

        # Calcula taxa (opcional)
        if self.estrategiaTaxa:
            transacao["taxa"] = self.calcularTaxa(animal)

        return transacao

    def registrarDevolucao(self, transacao, animal, adotante, motivo):
        if animal.status != "adotado":
            raise ValueError("A devolução só pode ocorrer para animais adotados.")

        data_dev = datetime.now()

        animal.alterarStatus("disponível")
        animal.registrarEvento("devolução", {
            "motivo": motivo,
            "data": data_dev.isoformat()
        })

        adotante.adicionarHistorico({
            "evento": "devolução",
            "animalId": animal.id,
            "motivo": motivo,
            "data": data_dev.isoformat()
        })

        transacao["dataDevolucao"] = data_dev.isoformat()
        transacao["motivoDevolucao"] = motivo

        return transacao

    def gerarContrato(self, transacao, animal, adotante):
        return {
            "contratoId": str(uuid.uuid4()),
            "animalId": animal.id,
            "adotanteId": adotante.id,
            "data": datetime.now().isoformat(),
            "termos": "O adotante se compromete a cuidar do animal..."
        }

    def calcularTaxa(self, animal):
        return self.estrategiaTaxa(animal)
