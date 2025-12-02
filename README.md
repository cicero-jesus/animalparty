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

As classes `Cachorro` e `Gato` herdam de `Animal`, removendo a necessidade de informar `especie` ao instanciar.

---

## 👤 **Adotante**

Possui:

- Dados cadastrais  
- Políticas de elegibilidade e compatibilidade  
- Histórico 
- Cálculo de elegibilidade  
- Cálculo de compatibilidade  

Agora o construtor aceita os campos adicionais carregados do JSON:

- `elegivel`
- `ptsCompatib`
- `historico`

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