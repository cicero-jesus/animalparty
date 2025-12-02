import json
import uuid
import os
from datetime import datetime

class TransacaoRepo:

    def __init__(self, file_path="data/transacoes.json"):
        """
        Inicializa o repositório garantindo que:
        - a pasta existe
        - o arquivo JSON existe
        - se estiver vazio, inicializa com []
        """
        # Caminho absoluto baseado no arquivo atual
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DATA_DIR = os.path.join(BASE_DIR, "data")

        # Garante que a pasta existe
        os.makedirs(DATA_DIR, exist_ok=True)

        # Caminho final do arquivo
        self.file_path = os.path.join(DATA_DIR, "transacoes.json")

        # Se arquivo não existir ou estiver vazio → cria
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

        # Carrega dados
        self.transacoes = self.load()

    # Carregar JSON
    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)

        except json.JSONDecodeError:
            # Arquivo corrompido → sobrescreve com lista vazia
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)
            return []

    # Salvar JSON
    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.transacoes, f, indent=4, ensure_ascii=False)

    # Criar transação
    def add(self, transacao: dict):
        """Adiciona uma transação (reserva / adoção / devolução)."""
        if "id" not in transacao:
            transacao["id"] = str(uuid.uuid4())
        self.transacoes.append(transacao)
        self.save()

    # Atualizar
    def update(self, transacao):
        """Substitui a transação com o mesmo ID."""
        for i, t in enumerate(self.transacoes):
            if t["id"] == transacao["id"]:
                self.transacoes[i] = transacao
                self.save()
                return
        raise ValueError("Transação não encontrada para atualização.")

    # Excluir
    def delete(self, transacao_id):
        self.transacoes = [t for t in self.transacoes if t["id"] != transacao_id]
        self.save()

    # Buscar por ID
    def findById(self, transacao_id):
        for t in self.transacoes:
            if t["id"] == transacao_id:
                return t
        return None

    # Listar por adotante
    def findByAdotante(self, adotante_id):
        return [t for t in self.transacoes if t.get("adotanteId") == adotante_id]

    # Listar por animal
    def findByAnimal(self, animal_id):
        return [t for t in self.transacoes if t.get("animalId") == animal_id]
