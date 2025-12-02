import json
import os
from base.adotante import Adotante

class AdotanteRepo:

    def __init__(self, caminho_json="data/adotantes.json"):
        self.caminho = caminho_json

        # Garante que o arquivo existe
        if not os.path.exists(self.caminho):
            os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
            with open(self.caminho, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        self.adotantes = self.load()

    # Carregar JSON
    def load(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Adotante(**a) for a in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    # Salvar JSON

    def save(self):
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump([a.__dict__ for a in self.adotantes], f, indent=4, ensure_ascii=False)

    # Criar
    def add(self, adotante: Adotante):
        self.adotantes.append(adotante)
        self.save()

    # Atualizar
    def update(self, adotante: Adotante):
        for i, a in enumerate(self.adotantes):
            if a.id == adotante.id:
                self.adotantes[i] = adotante
                self.save()
                return True
        return False

    # Excluir
    def delete(self, id):
        self.adotantes = [a for a in self.adotantes if a.id != id]
        self.save()

    # Buscar por ID
    def findById(self, id):
        for a in self.adotantes:
            if a.id == id:
                return a
        return None

    # Listar todos
    def findAll(self):
        return self.adotantes
