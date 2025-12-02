import json

class carregarSettings:

    @staticmethod
    def carregar_elegibilidade(caminho):
        with open(caminho, "r") as f:
            return json.load(f)

    @staticmethod
    def carregar_compatibilidade(caminho):
        with open(caminho, "r") as f:
            return json.load(f)
