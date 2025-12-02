from base.animal import Animal

class Gato(Animal):

    def __init__(
        self, 
        id, 
        nome, 
        raca, 
        sexo, 
        idadeMeses, 
        porte, 
        temperamento,
        status="recem-chegado",
        historicoEventos=None,
        dataEntrada=None,
        dataAdocao=None
    ):
        super().__init__(
            id=id,
            especie="gato",
            raca=raca,
            nome=nome,
            sexo=sexo,
            idadeMeses=idadeMeses,
            porte=porte,
            temperamento=temperamento,
            status=status,
            historicoEventos=historicoEventos,
            dataEntrada=dataEntrada,
            dataAdocao=dataAdocao
        )
