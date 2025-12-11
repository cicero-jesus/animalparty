from datetime import datetime

class Animal:
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
    """

    STATUS_VALIDOS = ["recem-chegado", "quarentena", "disponivel", "reservado", "adotado", "inadotavel"]
    
    def __init__(self, id, especie, raca, nome, sexo, idadeMeses,
                 porte, temperamento, status="recem-chegado",
                 historicoEventos=None, dataEntrada=None, dataAdocao=None):

        self.id = id
        self.especie = especie
        self.raca = raca
        self.nome = nome
        self.sexo = sexo
        self.idadeMeses = idadeMeses
        self.porte = porte               # P/M/G
        self.temperamento = temperamento # dócil, calmo, arisco...
        
        # Valida status inicial
        if status not in self.STATUS_VALIDOS:
            raise ValueError(f"Status inválido: {status}")
        self.status = status

        # Histórico
        self._historico = historicoEventos if historicoEventos else []

        # Datas para registro
        self.dataEntrada = dataEntrada if dataEntrada else datetime.now().isoformat()
        self.dataAdocao = dataAdocao

        # Registrar entrada
        self.registrarEvento("Entrada no sistema.")

    @property
    def historicoEventos(self):
        return tuple(self._historico)

    def registrarEvento(self, tipo, dados=None):
        evento = {
        "Tempo": datetime.now().isoformat(),
        "tipo": tipo,
        "dados": dados if dados else {}
    }
        self._historico.append(evento)

    def alterarStatus(self, novo_status):
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError(f"Status '{novo_status}' não é permitido.")
        
        antigo = self.status
        self.status = novo_status
        self.registrarEvento(f"Status alterado de '{antigo}' para '{novo_status}'.")

        # Marcar adoção
        if novo_status == "adotado":
            self.dataAdocao = datetime.now().isoformat()

    def quarentena(self):
        if self.status not in ["recem-chegado"]:
            raise ValueError("Apenas animais recém-chegados podem entrar em quarentena.")
        self.alterarStatus("quarentena")

    def liberarParaAdocao(self):
        if self.status not in ["quarentena"]:
            raise ValueError("Animal deve estar em quarentena antes de ser liberado.")
        self.alterarStatus("disponivel")

    def reservar(self):
        if self.status != "disponivel":
            raise ValueError("Somente animais disponíveis podem ser reservados.")
        self.alterarStatus("reservado")

    def adotar(self):
        if self.status not in ["reservado"]:
            raise ValueError("Somente animais reservados podem ser adotados.")
        self.alterarStatus("adotado")

    def marcarComoInadotavel(self, motivo=""):
        self.alterarStatus("inadotavel")
        if motivo:
            self.registrarEvento(f"Marcado como inadotável: {motivo}")

    def calcularAdotabilidade(self):
        score = 100

        # Filhotes são muito adotáveis
        if self.idadeMeses < 6:
            score += 10

        # Animais muito idosos têm redução
        if self.idadeMeses > 120:
            score -= 20

        # Porte grande reduz adotabilidade
        if self.porte == "G":
            score -= 15

        # Temperamento arisco reduz bastante
        if self.temperamento == "arisco":
            score -= 25

        return max(0, min(100, score))

    def Dic_atr_animal(self):
        return {
            "id": self.id,
            "especie": self.especie,
            "raca": self.raca,
            "nome": self.nome,
            "sexo": self.sexo,
            "idadeMeses": self.idadeMeses,
            "porte": self.porte,
            "temperamento": self.temperamento,
            "status": self.status,
            "historicoEventos": self._historico,
            "dataEntrada": self.dataEntrada,
            "dataAdocao": self.dataAdocao
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            especie=data["especie"],
            raca=data["raca"],
            nome=data["nome"],
            sexo=data["sexo"],
            idadeMeses=data["idadeMeses"],
            porte=data["porte"],
            temperamento=data["temperamento"],
            status=data.get("status", "disponivel"),
            historicoEventos=data.get("historicoEventos", []),
            dataEntrada=data.get("dataEntrada"),
            dataAdocao=data.get("dataAdocao")
        )

    def __str__(self):
        return f"{self.especie} {self.nome} ({self.porte}) - Status: {self.status}"