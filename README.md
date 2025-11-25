# DESCRIÇÃO DO PROJETO E OBJETIVOS
## 🐱 O que é a AnimalParty?
A AnimalParty é um sistema de adoções de animais pensado para a resolução de um problema proposto pela disciplina de Programação Orientada a Obejetos (POO), e tem como objetivo gerenciar o cadastro e reserva de animais, realizar a triagem de adotantes, manipular adoções e devoluções e gerar relatórios do histórico de adoção dos bichanos.
----
# 📚 ESTRUTURA DE CLASSES
| Classe| Atributos| Métodos| Relacionamentos|
|:---|:---|:---|:---|
| **Animal**          | id, especie, raca, nome, sexo, idadeMeses, porte (P/M/G), temperamento (lista), status, historicoEventos (lista), dataEntrada, dataAdocao | criar(), atualizar(), excluir(), registrarEvento(), alterarStatus(), calcularAdotabilidade(), Quarentena(), marcarComoInadotavel() | Relacionado a Adotante (reservas/adoções), possui eventos de histórico, usado em Relatorio|
| **Adotante**        | id, nome, idade, moradia, areaUtil, experienciaPets, criancasEmCasa, outrosAnimais, ptsCompatib, elegivel | criar(), atualizar(), excluir(), validarElegibilidade(), calcularCompatibilidade(), reservarAnimal(), adotarAnimal(), adicionarHistorico, obterHistorico | Relaciona-se com Animal (reserva/adoção), relacionado a Adotar_Devolver|
| **Relatorio**       | id, tipo, periodo, dadosGerados, filtros | gerarTop5Adotaveis(), gerarTaxaAdocaoPorEspecie(), gerarTaxaAdocaoPorPorte(), gerarTempoMedioEntradaAdocao(), gerarDevolucoesPorMotivo() | Usa dados de Animal, Adotante e Adotar_Devolver|
| **Adotar_Devolver** | id, animalId, adotanteId, dataReserva, dataExpiracaoReserva, dataAdocao, dataDevolucao, motivoDevolucao, contrato, estrategiaTaxa | reservar(), expirarReserva(), efetivarAdocao(), gerarContrato(), calcularTaxa(), registrarDevolucao(), enviarNotProxFila() | Liga Animal ↔ Adotante, gera eventos no histórico do animal, base para Relatorio|

----

### 💻 RODANDO NO PC
**COLE NO TERMINAL**📋
```
git clone https://github.com/cicero-jesus/animalparty.git
```
----

**ENTRE NA PASTA**📂
```
cd .../animalparty
```
> OBS: ".../" TRATA-SE DO DIRETORIO AONDE O REPOSITORIO FOI CLONADO. *Ex: /home/usuario/Downloads/animalparty*

----
**EXECUTE O ARQUIVO main.py**🐍
```
python3 main.py
```
----