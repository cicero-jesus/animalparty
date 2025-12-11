import json
import os

class CarregarSettings:

    @staticmethod
    def _caminho_absoluto(nome):
        base = os.path.dirname(__file__)       
        raiz = os.path.dirname(base)              
        return os.path.join(raiz, nome)

    @staticmethod
    def carregar(caminho):
        arquivo = CarregarSettings._caminho_absoluto(caminho)
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def carregar_elegibilidade(caminho):
        settings = CarregarSettings.carregar(caminho)
        return settings["Elegibilidade"]

    @staticmethod
    def carregar_compatibilidade(caminho):
        settings = CarregarSettings.carregar(caminho)
        return {
            "pesos": settings["pesos"],
            "regras": settings["regras"]
        }
