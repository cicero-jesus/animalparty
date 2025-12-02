from servicos.animal_repo import AnimalRepo
from servicos.adotante_repo import AdotanteRepo
from servicos.transacoes_repo import TransacaoRepo
from servicos.relatorios_repo import RelatorioRepo

from base.adotar_devolver import adotarDevolver

from base.cachorro import Cachorro
from base.gato import Gato
from base.adotante import Adotante

from datetime import datetime
import statistics

def menu_principal():
    print("\n===== SISTEMA DE ADOÇÃO =====")
    print("1. Cadastrar Animal")
    print("2. Cadastrar Adotante")
    print("3. Reservar Animal")
    print("4. Efetivar Adoção")
    print("5. Registrar Devolução")
    print("6. Listar Animais")
    print("7. Listar Adotantes")
    print("8. Relatórios")
    print("0. Sair")
    return input("Escolha: ")


def menu_relatorios():
    print("\n===== RELATÓRIOS =====")
    print("1. Animais Disponíveis")
    print("2. Animais Adotados")
    print("3. Reservas Ativas")
    print("4. Reservas Expiradas")
    print("5. Devoluções Registradas")
    print("6. Top 5 Mais Adotáveis")
    print("7. Taxa de Adoções por Espécie/Porte")
    print("8. Tempo Médio Entre Entrada e Adoção")
    print("9. Devoluções por Motivo")
    print("0. Voltar")
    return input("Escolha: ")

def main():

    animalRepo = AnimalRepo("animalparty/data/animais.json")
    adotanteRepo = AdotanteRepo("animalparty/data/adotantes.json")
    transacaoRepo = TransacaoRepo("animalparty/data/transacoes.json")

    relatorios = RelatorioRepo(animalRepo, transacaoRepo, adotanteRepo)
    service = adotarDevolver()

    while True:
        esc = menu_principal()

        if esc == "1":
            especie = input("Espécie (cachorro/gato): ").lower()
            nome = input("Nome: ")
            raca = input("Raça: ")
            sexo = input("Sexo: ")
            idade = int(input("Idade em meses: "))
            porte = input("Porte (pequeno/médio/grande): ")
            temperamento = input("Temperamento: ")

            id_ = len(animalRepo.animais) + 1

            if especie == "cachorro":
                animal = Cachorro(id_, nome, raca, sexo, idade, porte, temperamento, status="disponivel")
            else:
                animal = Gato(id_, nome, raca, sexo, idade, porte, temperamento, status="disponivel")

            animalRepo.add(animal)
            print("Animal cadastrado.")

        elif esc == "2":
            nome = input("Nome: ")
            idade = int(input("Idade: "))
            criancas = input("Crianças em casa (sim/nao): ").lower() == "sim"
            moradia = input("Moradia (casa/apto): ")
            area = float(input("Área útil (m²): "))
            experiencia = input("Experiência com pets (sim/nao): ").lower() == "sim"
            outros = input("Possui outros animais? (sim/nao): ").lower() == "sim"

            adotante = Adotante(
                len(adotanteRepo.adotantes) + 1,
                nome, idade, criancas, moradia, area,
                experiencia, outros,
                ptsCompatib=0,
                elegivel=False
            )

            adotanteRepo.add(adotante)
            print("Adotante cadastrado.")

        elif esc == "3":
            animalId = int(input("ID do animal: "))
            adotanteId = int(input("ID do adotante: "))

            animal = animalRepo.findById(animalId)
            adotante = adotanteRepo.findById(adotanteId)

            transacao = service.reservar(adotante, animal)

            transacaoRepo.add(transacao)
            animalRepo.save()
            adotanteRepo.save()

            print("Reserva registrada.")

        elif esc == "4":
            tId = input("ID da transação: ")

            trans = transacaoRepo.findById(tId)
            animal = animalRepo.findById(trans["animalId"])
            adotante = adotanteRepo.findById(trans["adotanteId"])

            service.efetivarAdocao(trans, animal, adotante)

            transacaoRepo.update(trans)
            animalRepo.save()
            adotanteRepo.save()

            print("Adoção efetivada.")

        elif esc == "5":
            tId = input("ID da transação: ")
            motivo = input("Motivo da devolução: ")

            trans = transacaoRepo.findById(tId)
            animal = animalRepo.findById(trans["animalId"])
            adotante = adotanteRepo.findById(trans["adotanteId"])

            service.registrarDevolucao(trans, animal, adotante, motivo)

            transacaoRepo.update(trans)
            animalRepo.save()
            adotanteRepo.save()

            print("Devolução registrada.")

        elif esc == "6":
            for a in animalRepo.animais:
                print(a)

        elif esc == "7":
            for a in adotanteRepo.adotantes:
                print(a)

        elif esc == "8":
            r = menu_relatorios()

            # Animais disponíveis
            if r == "1":
                for a in relatorios.animaisDisponiveis():
                    print(a)

            # Animais adotados
            elif r == "2":
                for a in relatorios.animaisAdotados():
                    print(a)

            # Reservas Ativas
            elif r == "3":
                print(relatorios.reservasAtivas())

            # Reservas Expiradas
            elif r == "4":
                print(relatorios.reservasExpiradas())

            # Devoluções
            elif r == "5":
                print(relatorios.devolucoes())
            # Top 5 adotáveis
            elif r == "6":
                animais_ordenados = sorted(
                    [a for a in animalRepo.animais if hasattr(a, "ptsCompatib")],
                    key=lambda x: x.ptsCompatib,
                    reverse=True
                )
                top5 = animais_ordenados[:5]
                for a in top5:
                    print(f"{a.nome} - Compatibilidade: {a.ptsCompatib}")

            elif r == "7":
                total = len(animalRepo.animais)
                adotados = relatorios.animaisAdotados()

                estatistica = {}

                for a in animalRepo.animais:
                    chave = f"{a.especie}-{a.porte}"
                    if chave not in estatistica:
                        estatistica[chave] = {"total": 0, "adotados": 0}
                    estatistica[chave]["total"] += 1

                for a in adotados:
                    chave = f"{a.especie}-{a.porte}"
                    estatistica[chave]["adotados"] += 1

                for cat, dados in estatistica.items():
                    taxa = (dados["adotados"] / dados["total"]) * 100 if dados["total"] else 0
                    print(f"{cat}: {taxa:.2f}% de adoção")

            elif r == "8":
                tempos = []
                for a in relatorios.animaisAdotados():
                    if a.dataEntrada and a.dataAdocao:
                        dt1 = datetime.fromisoformat(a.dataEntrada)
                        dt2 = datetime.fromisoformat(a.dataAdocao)
                        tempos.append((dt2 - dt1).days)

                if tempos:
                    print(f"Tempo médio: {statistics.mean(tempos):.2f} dias")
                else:
                    print("Nenhum dado disponível.")

            elif r == "9":
                motivos = {}
                devs = relatorios.devolucoes()

                for t in devs:
                    m = t["motivoDevolucao"]
                    motivos[m] = motivos.get(m, 0) + 1

                for mot, qnt in motivos.items():
                    print(f"{mot}: {qnt} devoluções")

        elif esc == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()