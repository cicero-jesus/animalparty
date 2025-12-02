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
    """

    def __init__(
        self,
        id,
        nome,
        idade,
        moradia,
        areaUtil,
        experienciaPets,
        criancasEmCasa,
        outrosAnimais,
        politica_elegibilidade=None,
        politica_compatibilidade=None,
        elegivel=False,
        ptsCompatib=0,
        historico=None,
        animaisReservados=None,
        animaisAdotados=None 
    ):

        self.id = id

        # Nome
        self.__nome = nome

        # Dados básicos
        self.idade = idade
        self.moradia = moradia
        self.areaUtil = areaUtil
        self.experienciaPets = experienciaPets
        self.outrosAnimais = outrosAnimais

        # Crianças em casa
        self.__criancasEmCasa = criancasEmCasa

        # Políticas opcionais
        self.politica_elegibilidade = politica_elegibilidade
        self.politica_compatibilidade = politica_compatibilidade

        # Resultados calculados
        self.elegivel = elegivel
        self.ptsCompatib = ptsCompatib

        # Histórico
        self._historico = historico if historico is not None else []

        # Listas vindas do JSON
        self.animaisReservados = animaisReservados or []
        self.animaisAdotados = animaisAdotados or []  

    # PROPRIEDADES

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, n):
        if not n:
            raise ValueError("Nome não pode ser vazio.")
        self.__nome = n

    @property
    def criancasEmCasa(self):
        return self.__criancasEmCasa

    @criancasEmCasa.setter
    def criancasEmCasa(self, valor):
        if type(valor) not in [bool, int]:
            raise ValueError("Você deve informar True/False ou o número de crianças.")
        self.__criancasEmCasa = valor

    # LÓGICAS DE NEGÓCIO

    def validarElegibilidade(self):
        if self.politica_elegibilidade is None:
            raise RuntimeError("Política de elegibilidade não carregada.")

        pol = self.politica_elegibilidade
        motivos = []

        if self.areaUtil < pol["area_min"]:
            motivos.append("Área insuficiente.")

        if pol["exige_experiencia"] and not self.experienciaPets:
            motivos.append("Experiência prévia obrigatória.")

        if not pol["permite_criancas"] and self.criancasEmCasa:
            motivos.append("Presença de crianças não é permitida.")

        self.elegivel = len(motivos) == 0

        self.adicionarHistorico(
            f"Elegibilidade: {'Aprovado' if self.elegivel else 'Reprovado'}"
        )

        return (self.elegivel, motivos)

    def calcularCompatibilidade(self, animal):
        if self.politica_compatibilidade is None:
            raise RuntimeError("Política de compatibilidade não carregada.")

        pes = self.politica_compatibilidade["pesos"]
        reg = self.politica_compatibilidade["regras"]

        score = 0

        # Porte
        if self.moradia == "apto" and animal.porte == "G":
            score += reg["porte_grande_em_apto"] * pes["porte_moradia"]
        else:
            score += reg["porte_adequado"] * pes["porte_moradia"]

        # Energia
        if animal.energia == "alta" and self.idade > 60:
            score += reg["energia_alta_adotante_idoso"] * pes["idade_energia"]
        else:
            score += reg["energia_ok"] * pes["idade_energia"]

        # Experiência
        score += (reg["com_experiencia"] if self.experienciaPets else reg["sem_experiencia"]) \
            * pes["experiencia"]

        # Crianças
        if self.criancasEmCasa and animal.temperamento == "arisco":
            score += reg["criancas_com_animal_arisco"] * pes["criancas"]
        else:
            score += reg["criancas_ok"] * pes["criancas"]

        self.ptsCompatib = round(score)
        self.adicionarHistorico(f"Compatibilidade com {animal.nome}: {self.ptsCompatib}")

        return self.ptsCompatib

    # HISTÓRICO

    def adicionarHistorico(self, evento):
        self._historico.append(evento)

    def obterHistorico(self):
        return list(self._historico)

    # EXPORTAÇÃO PARA JSON

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.__nome,
            "idade": self.idade,
            "moradia": self.moradia,
            "areaUtil": self.areaUtil,
            "experienciaPets": self.experienciaPets,
            "criancasEmCasa": self.__criancasEmCasa,
            "outrosAnimais": self.outrosAnimais,
            "elegivel": self.elegivel,
            "ptsCompatib": self.ptsCompatib,
            "historico": self._historico,
            "animaisReservados": self.animaisReservados,
            "animaisAdotados": self.animaisAdotados 
        }

    def __str__(self):
        return f"Adotante {self.nome} (Elegível: {self.elegivel}, Compat: {self.ptsCompatib})"