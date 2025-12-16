# 🐾 AnimalParty – Sistema de Adoção, Reservas e Relatórios

AnimalParty é um sistema em Python para gerenciar **animais**, **adotantes**, **transações** (reservas, adoções e devoluções) e **relatórios gerenciais**.

O projeto utiliza arquivos `.json` como armazenamento e segue um padrão de repositórios (Repos) para manipulação dos dados.

---

# 📁 Estrutura Atual do Projeto
```
animalparty/
│
├── base/
│ ├── animal.py
│ ├── gato.py
│ ├── cachorro.py
│ ├── adotar_devolver.py
│ └── adotante.py
│
├── data/
│ ├── animais.json
│ ├── adotantes.json
│ ├── transacoes.json
│ └── settings.json
│
├── servicos/
│ ├── animal_repo.py
│ ├── adotante_repo.py
│ ├── transacoes_repo.py
│ ├── relatorios_repo.py
│ └── carregar_settings.py
│
└── main.py
```

---

# 📌 Principais Componentes

## 🐶 **Animal, Cachorro e Gato**
A classe `Animal` é abstrata e representa os atributos básicos:

- id  
- espécie  
- raça  
- nome  
- sexo  
- idadeMeses  
- porte  
- temperamento  
- status  
- histórico de eventos  
- dataEntrada
- dataAdocao

As classes `Cachorro` e `Gato` herdam de `Animal`, removendo a necessidade de informar `especie` ao instanciar.

---

## 👤 **Adotante**

Possui os atributos: 

- id  
- nome 
- idade 
- moradia
- areautil  
- experienciaPets
- criancasEmCasa
- outrosAnimais
- politica_elegibilidade
- politica_compatibilidade
- elegivel
- ptsCompatib
- historico
- animaisReservados
- animaisAdotados

Representa um `adotante` envolvido no processo de reservas/adoções e mantém um histórico de eventos utilizado para geraçãode relatórios.

---

## 📦 Repositórios

### ✔ AnimalRepo  
Carrega, atualiza e salva animais no `animais.json`, tratando diferenças de campos com limpeza automática antes da criação das classes.

### ✔ AdotanteRepo  
Gerencia adotantes no `adotantes.json`, criando objetos `Adotante` completos.

### ✔ TransacaoRepo  
Gerencia reservas, adoções e devoluções.

### ✔ RelatorioRepo  
Gera:

- Animais disponíveis  
- Animais adotados  
- Reservas ativas / expiradas  
- Devoluções  
- Adoções por período  
- Histórico por adotante  

---

### 💻 RODANDO NO PC
----
**CRIE UMA PASTA PARA SALVAR📁**
- No Linux 🐧 (Via Terminal)
> Ex.:
``` 
~/Documentos: mkdir POO-PROJECT
```
- No Windows 🪟
> Abra o gerenciador arquivos, entre em uma pasta de sua escolha e crie uma nova pasta com o botão direito do mouse > novo > pasta, e renomeie para POO-PROJECT, por exemplo.
----
**ENTRE NA PASTA**📂
```
cd .../POO-PROJECT
```
> OBS: ".../" TRATA-SE DO DIRETÓRIO AONDE A PASTA FOI CRIADA. *Ex: /home/usuario/Downloads/POO-PROJECT* 
---- 
**COLE NO TERMINAL**📋
```
git clone https://github.com/cicero-jesus/animalparty.git
```
---- 
**EXECUTE O ARQUIVO main.py**🐍
```
python3 animalparty/main.py 
```
>OBS.: Necessário ter o [python](https://www.python.org/downloads/) instalado na máquina, em sua versão 3.x.
----