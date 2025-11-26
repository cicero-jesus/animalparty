import adotante
import adotar_devolver
import req_relatorio
import animal

""" Arquivo principal do módulo media, realiza as chamadas de outras classes, 
    e é o arquivo principal para execução no teminal.
    Classes disponíveis:
    - Animal
    - Adotante
    - Adotar_Devolver
    - Relatorio
    """
identificador = 1
while True:
    print("\nBem-vindo ao sistema de adoção de animais!\n")
    print("Escolha uma opção:\n")
    print("1. Registrar Adotante\n")
    print("2. Atualizar Adotante\n")
    print("3. Excluir Adotante\n")
    print("4. Registrar Animal\n")
    print("5. Atualizar Animal\n")
    print("6. Excluir Animal\n")
    print("7. Registrar Adoção/Devolução\n")
    print("8. Gerar Relatório\n")
    print("9. Sair\n")

    escolha = input("Digite o número da opção desejada:\nR.> ")

    if escolha == '1': 
        nome = input("Digite o nome do adotante: ")
        idade = int(input("Digite a idade do adotante: "))
        criancasEmCasa = input("Há crianças em casa? (sim/não): ")
        moradia = input("Tipo de moradia (casa/apartamento): ")
        areaUtil = float(input("Área útil disponível (em m²): "))
        experienciaPets = input("Experiência prévia com animais (sim/não): ")
        outrosAnimais = input("Há outros animais no domicílio? (sim/não): ")
        adt = adotante.Adotante(identificador, nome, idade, criancasEmCasa, moradia, areaUtil, experienciaPets, outrosAnimais)
        adt.criar()
        identificador += 1

    elif escolha == '2':
        pass
    elif escolha == '3':
        pass
    elif escolha == '4':
        pass
    elif escolha == '5':
        pass
    elif escolha == '6':
        pass
    elif escolha == '7':
        pass
    elif escolha == '8':
        req_relatorio.Relatorio().gerarInfoAnimais()
    elif escolha == '9':
        print("Saindo do sistema. Até mais!")
        break
    else:
        print("Opção inválida. Por favor, tente novamente.")