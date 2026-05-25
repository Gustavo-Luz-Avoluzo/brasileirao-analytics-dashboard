
# 🇧🇷 Brasileirão Analytics Dashboard

Dashboard profissional de análise de dados do **Campeonato Brasileiro Série A 2026**, construído com uma stack completa de Engenharia e Análise de Dados.

<img width="1344" height="753" alt="dash brasileirao" src="https://github.com/user-attachments/assets/bb6a7351-d32c-4d0b-bbc9-c0ff684ad123" />
---

## 📊 Sobre o Projeto

Este projeto coleta, processa e visualiza dados reais do Brasileirão Série A em tempo real, utilizando uma arquitetura de pipeline de dados completa — da ingestão à visualização final no Power BI.

O objetivo é demonstrar na prática habilidades em **Engenharia de Dados**, **Analytics** e **Business Intelligence**, cobrindo toda a jornada dos dados desde a API até o dashboard interativo.

---

## 🖥️ Dashboard

O dashboard foi desenvolvido no **Power BI Desktop** com fundo customizado em HTML/CSS, contendo:

- 📋 **Tabela de Classificação** — posição, time, pontos, aproveitamento e logos dos clubes
- ⚽ **Próximos Jogos** — agenda atualizada da rodada
- 🏆 **Artilheiros** — ranking de gols e assistências
- 📈 **Evolução por Rodada** — gráfico de pontos acumulados por time

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
|--------|-----------|
| Linguagem | Python 3.14 |
| Banco de Dados | PostgreSQL 18 |
| Containerização | Docker + Docker Compose |
| Orquestração | Apache Airflow 2.7 |
| Visualização | Power BI Desktop |
| Interface | HTML + CSS customizado |
| API de Dados | football-data.org |

---

## 🏗️ Arquitetura do Pipeline

```
football-data.org API
        ↓
  Python (coleta)
        ↓
  PostgreSQL (armazenamento)
        ↓
  Apache Airflow (orquestração diária)
        ↓
  CSV Export
        ↓
  Power BI (visualização)
```

---

## 📁 Estrutura do Projeto

```
brasileirao-analytics/
│
├── dags/
│   └── brasileirao_dag.py          # DAG do Airflow (agendamento diário)
│
├── scripts/
│   └── brasileirao_pipeline.py     # Pipeline de coleta e armazenamento
│
├── exportar.py                     # Exporta tabelas do banco para CSV
├── docker-compose.yml              # PostgreSQL + Airflow em containers
├── requirements.txt                # Dependências Python
├── .env.example                    # Exemplo de variáveis de ambiente
└── .gitignore                      # Arquivos ignorados pelo Git
```

---

## ⚙️ Como Executar

### Pré-requisitos

- Python 3.10+
- Docker Desktop instalado e rodando
- Conta gratuita em [football-data.org](https://www.football-data.org)
- Power BI Desktop

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/brasileirao-analytics.git
cd brasileirao-analytics
```

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`:

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais:

```
FOOTBALL_DATA_TOKEN=seu_token_aqui
DB_PASSWORD=sua_senha_aqui
```

### 3. Instale as dependências Python

```bash
pip install -r requirements.txt
```

### 4. Suba os containers

```bash
docker-compose up -d
```

### 5. Execute o pipeline manualmente

```bash
python scripts/brasileirao_pipeline.py
```

### 6. Exporte os dados para CSV

```bash
python exportar.py
```

### 7. Abra o Power BI

- Importe os arquivos CSV gerados (`classificacao.csv`, `artilheiros.csv`, `jogos.csv`)
- Use o arquivo `brasileirao_background.html` como fundo da página (exporte para PNG pelo Chrome)

### 8. Airflow (automação diária)

Acesse o painel do Airflow em `http://localhost:8080` e ative a DAG `brasileirao_pipeline`.

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz com as seguintes variáveis:

| Variável | Descrição |
|----------|-----------|
| `FOOTBALL_DATA_TOKEN` | Token da API football-data.org |
| `DB_PASSWORD` | Senha do PostgreSQL |

⚠️ **Nunca compartilhe seu token publicamente. O arquivo `.env` está no `.gitignore`.**

---

## 📡 API Utilizada

- **[football-data.org](https://www.football-data.org)** — API gratuita com dados do Brasileirão Série A
- Endpoints utilizados:
  - `/competitions/BSA/standings` — Classificação
  - `/competitions/BSA/scorers` — Artilheiros
  - `/competitions/BSA/matches` — Jogos

---


## 👨‍💻 Autor

**Gustavo Luz de Brito**
- Analista de Sistemas em formação
- Técnico em Banco de Dados (Etec)
- Tecnólogo em Análise e Desenvolvimento de Sistemas (Facens)
