from servicos.animal_repo import AnimalRepo
from servicos.adotante_repo import AdotanteRepo
from servicos.transacoes_repo import TransacaoRepo
from servicos.relatorios_repo import RelatorioRepo
from servicos.carregar_settings import CarregarSettings

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
                nome, idade, moradia, area, experiencia,
                criancas, outros
            )
            #Carregar Politicas
            politica_elegibilidade = CarregarSettings.carregar_elegibilidade("data/settings.json")
            politica_compatibilidade = CarregarSettings.carregar_compatibilidade("data/settings.json")

            # aplicar políticas
            adotante.politica_elegibilidade = politica_elegibilidade
            adotante.politica_compatibilidade = politica_compatibilidade

            # Valida Elegiblidade
            elegivel, motivos = adotante.validarElegibilidade()

            print("Elegível?" , elegivel)
            if not elegivel:
                print("Motivos:", motivos)

            adotanteRepo.add(adotante)
            print("Adotante cadastrado, após verificação de elegibilidade.")

        elif esc == "3":
            animalId = int(input("ID do animal: "))
            adotanteId = int(input("ID do adotante: "))

            animal = animalRepo.findById(animalId)
            adotante = adotanteRepo.findById(adotanteId)

            #Carregar Politicas
            #print(CarregarSettings._caminho_absoluto("data/settings.json"))
            politica_elegibilidade = CarregarSettings.carregar_elegibilidade("data/settings.json")
            politica_compatibilidade = CarregarSettings.carregar_compatibilidade("data/settings.json")

            # Reaplicar políticas ao carregar
            adotante.politica_elegibilidade = politica_elegibilidade
            adotante.politica_compatibilidade = politica_compatibilidade

            # garantir elegibilidade atualizada
            adotante.validarElegibilidade()

            # calcular compatibilidade com o animal
            try:
                adotante.calcularCompatibilidade(animal)
            except ValueError as e:
                print(f"Erro: {e}")
                continue

            # Tentativa de reserva
            try:
                transacao = service.reservar(adotante, animal)
                transacaoRepo.add(transacao)
                print("Reserva registrada.")
            except ValueError as e: 
                print(f"Erro ao reservar: {e}")

            animalRepo.save()
            adotanteRepo.save()


        elif esc == "4":
            reservas = relatorios.reservasAtivasDetalhadas()

            if not reservas:
                print("Não há reservas ativas.")
                continue

            print("Reservas ativas:")
            for r in reservas:
                print(
                    f"Animal: {r['animalNome']} (ID {r['animalId']}) | "
                    f"Adotante: {r['adotanteNome']} (ID {r['adotanteId']})"
                )

            animalId = int(input("Informe o ID do animal: "))
            adotanteId = int(input("Informe o ID do adotante: "))

            trans = transacaoRepo.findReservaAtiva(animalId, adotanteId)

            if not trans:
                print("Reserva não encontrada.")
                continue


            #trans = transacaoRepo.findById(tId)
            animal = animalRepo.findById(trans["animalId"])
            adotante = adotanteRepo.findById(trans["adotanteId"])

            service.efetivarAdocao(trans, animal, adotante)

            transacaoRepo.update(trans)
            animalRepo.save()
            adotanteRepo.save()

            print("Adoção efetivada.")

        elif esc == "5":

            adocoes = relatorios.adocoesAtivasDetalhadas()

            if not adocoes:
                print("Não há adoções ativas para devolução.")
                continue

            print("\nAdoções ativas:")
            for i, a in enumerate(adocoes, 1):
                print(
                    f"{i}. Animal #{a['animalId']} - {a['animalNome']} | "
                    f"Adotante #{a['adotanteId']} - {a['adotanteNome']}"
                )

            op = int(input("Escolha a adoção para devolver: ")) - 1
            motivo = input("Motivo da devolução: ")

            selecionada = adocoes[op]

            trans = selecionada["transacao"]

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
                resultado = relatorios.devolucoes()
                print(f"Total de devoluções: {resultado['total']}")
                print("IDs das devoluções:")
                for i in resultado["ids"]:
                    print("-", i)

            # Top 5 adotáveis
            elif r == "6":
                ranking = []

                for a in animalRepo.animais:
                    if a.status != "disponivel":
                        continue

                    pontos = 0

                    # espécie
                    if a.especie == "cachorro":
                        pontos += 2

                    # idade (até 2 anos)
                    if a.idadeMeses <= 24:
                        pontos += 2

                    # porte
                    if a.porte in ("pequeno", "medio"):
                        pontos += 1

                    # temperamento
                    if a.temperamento == "calmo":
                        pontos += 1

                    ranking.append((pontos, a))

                if not ranking:
                    print("Nenhum animal disponível para ranking.")
                else:
                    ranking.sort(key=lambda x: x[0], reverse=True)
                    top5 = ranking[:5]

                    print("\nTop 5 animais mais adotáveis:")
                    for pos, (pts, a) in enumerate(top5, start=1):
                        print(f"{pos}º {a.nome} ({a.especie}) - {pts} pontos")


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

                for animal in animalRepo.animais:
                    adocoes_validas = []

                    for t in transacaoRepo.transacoes:
                        if t.get("dataAdocao") and t["animalId"] == animal.id:
                            dt_adocao = datetime.fromisoformat(t["dataAdocao"])
                            dt_entrada = datetime.fromisoformat(animal.dataEntrada)

                            # regra de negócio: adoção após entrada
                            if dt_adocao >= dt_entrada:
                                # considerar apenas a última adoção ativa
                                if t.get("dataDevolucao") is None:
                                    adocoes_validas.append(dt_adocao)

                    if not adocoes_validas:
                        continue

                    # última adoção válida
                    ultima_adocao = max(adocoes_validas)

                    delta = ultima_adocao - datetime.fromisoformat(animal.dataEntrada)
                    dias = delta.total_seconds() / 86400  # ← DIAS COM DECIMAL

                    tempos.append(dias)

                if tempos:
                    print(
                        f"Tempo médio entre entrada e última adoção válida: "
                        f"{statistics.mean(tempos):.2f} dias"
                    )
                else:
                    print("Nenhum dado válido para cálculo.")

            elif r == "9":
                ids = relatorios.devolucoes()["ids"]

                if not ids:
                    print("Não há devoluções registradas.")
                    continue

                motivos = {}
                for t in transacaoRepo.transacoes:
                    if t["id"] in ids:
                        m = t.get("motivoDevolucao", "Não informado")
                        motivos[m] = motivos.get(m, 0) + 1

                print("\nDevoluções por motivo:")
                for mot, qnt in motivos.items():
                    print(f"{mot}: {qnt}")


        elif esc == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()