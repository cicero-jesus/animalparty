import json

from base.animal import Animal
from base.cachorro import Cachorro
from base.gato import Gato


class AnimalRepo:

    def __init__(self, file_path="data/animais.json"):
        self.file_path = file_path
        self.animais = self.load()

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            animais = []
            for a in data:

                # Remover atributos privados
                clean = {k: v for k, v in a.items() if not k.startswith("_")}

                especie = clean.get("especie")

                if especie == "cachorro":
                    # Remover especie antes de passar ao construtor Cachorro
                    clean.pop("especie", None)
                    animais.append(Cachorro(**clean))

                elif especie == "gato":
                    clean.pop("especie", None)
                    animais.append(Gato(**clean))

                else:
                    # Aqui o Animal base PRECISA de especie
                    if especie is None:
                        raise ValueError("Animal no JSON está sem campo 'especie'")
                    animais.append(Animal(**clean))

            return animais

        except FileNotFoundError:
            return []

    def save(self):
        from datetime import datetime
        def serialize(a):
            data = {}

            for k, v in a.__dict__.items():
                if k.startswith("_"):
                    continue

                if isinstance(v, datetime):
                    data[k] = v.isoformat()
                else:
                    data[k] = v

            return data


        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([serialize(a) for a in self.animais], f, ensure_ascii=False, indent=4)

    def add(self, animal):
        self.animais.append(animal)
        self.save()

    def update(self, animal):
        self.save()

    def findById(self, animal_id):
        for a in self.animais:
            if a.id == animal_id:
                return a
        return None