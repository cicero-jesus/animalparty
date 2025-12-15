import json
import uuid
from datetime import datetime
from datetime import datetime

class RelatorioRepo:

    def __init__(self, animalRepo, transacaoRepo, adotanteRepo):
        self.animalRepo = animalRepo
        self.transacaoRepo = transacaoRepo
        self.adotanteRepo = adotanteRepo

    # Animais disponíveis
    def animaisDisponiveis(self):
        return [a for a in self.animalRepo.animais if a.status == "disponivel"]

    # Animais adotados
    def animaisAdotados(self):
        return [a for a in self.animalRepo.animais if a.status == "adotado"]

    # Reservas ativas
    def reservasAtivas(self):
        lista = []
        now = datetime.now()
        for t in self.transacaoRepo.transacoes:
            if t["dataAdocao"] is None:  # ainda não virou adoção
                exp = datetime.fromisoformat(t["dataExpiracaoReserva"])
                if now < exp:
                    lista.append(t)
        return lista

    # Reservas expiradas
    def reservasExpiradas(self):
        lista = []
        now = datetime.now()
        for t in self.transacaoRepo.transacoes:
            if t["dataAdocao"] is None:
                exp = datetime.fromisoformat(t["dataExpiracaoReserva"])
                if now >= exp:
                    lista.append(t)
        return lista

    # Devoluções
    def devolucoes(self):
        devolucoes = [
        t for t in self.transacaoRepo.transacoes
        if t.get("dataDevolucao") is not None
    ]
        return {
        "total": len(devolucoes),
        "ids": [t["id"] for t in devolucoes]
    }

    # Adoções por período (YYYY-MM-DD)
    def adocoesPorPeriodo(self, dataInicial, dataFinal):
        i = datetime.fromisoformat(dataInicial)
        f = datetime.fromisoformat(dataFinal)

        resultado = []
        for t in self.transacaoRepo.transacoes:
            if t["dataAdocao"]:
                d = datetime.fromisoformat(t["dataAdocao"])
                if i <= d <= f:
                    resultado.append(t)
        return resultado

    # Histórico consolidado por adotante
    def historicoPorAdotante(self, adotante_id):
        adotante = self.adotanteRepo.findById(adotante_id)
        transacoes = self.transacaoRepo.findByAdotante(adotante_id)

        return {
            "adotante": adotante.nome,
            "transacoes": transacoes,
            "totalReservas": len([t for t in transacoes if t["dataAdocao"] is None]),
            "totalAdocoes": len([t for t in transacoes if t["dataAdocao"]]),
            "totalDevolucoes": len([t for t in transacoes if t["dataDevolucao"]])
        }

