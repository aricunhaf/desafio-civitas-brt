# 🚍 Desafio de Data Engineer - Civitas

Este repositório contém a implementação do desafio técnico para a vaga de **Engenheiro(a) de Dados** na [Civitas](https://civitas.rio/).  
O objetivo é construir uma **pipeline ELT em arquitetura Medallion (Bronze → Silver → Gold)**,  
utilizando **Prefect 1.4.1** e **Google Cloud (GCS + BigQuery)** para ingestão, armazenamento e transformação de dados do BRT em tempo real.

<a name="docs"/>

### Documentação e Testes

## 📋 Índice

- [Ambiente e Ferramentas](#tools)
- [Arquitetura](arquitecture)
  - [Arquitetura das Pipelines](#pipelines)
  - [Arquitetura das Queries](#dbt)
  - [Estrutura de Diretórios](#directories)
  - [Camadas de modelagem](#model)
  - [Documentação e Testes](#docs)
- [Setup do Ambiente de Desenvolvimento Local](#setup)
  - [1. Pré-requisitos](#setup1)
  - [2. Criação do ambiente virtual](#setup2)
  - [3. Instalar dependências](#setup3)
  - [4. Configuração do Docker](#setup4)
  - [5. Subir o Prefect Server Local e Iniciar o server](#setup5)
  - [6. Variáveis de ambiente e credenciais GCP](#setup6)

---
<a name="tools"/>

###  ⚙️ Ambiente e Ferramentas

| Componente | Versão | Função |
|-------------|---------|--------|
| **Python** | 3.10 | Linguagem principal |
| **Prefect** | 1.4.1 | Orquestração da pipeline |
| **Docker / Docker Compose** | 4.4.4 / 1.29.2 | Infraestrutura local e agente |
| **Google Cloud SDK** | latest | Armazenamento e consultas |
| **DBT (Data Build Tool)** | latest | Transformação de dados no BigQuery |
---
<a name="arquitecture"/>

## Arquitetura

<a name="pipelines"/>

### Arquitetura das Pipelines
Os pipelines seguem o padrão ELT orquestrado pelo Prefect.

<a name="dbt"/>

### Arquitetura das Queries (DBT)
As transformações de dados utilizam **DBT (Data Build Tool)**.

<a name="directories"/>

### Estrutura de Diretórios
dbt_project/
├── dbt_project.yml           # Configuração do projeto DBT
├── packages.yml              # Pacotes DBT externos (dbt_utils, dbt_expectations, elementary)
├── models/
│   ├── bronze/               # Camada Bronze - dados brutos (tabela externa BigQuery)
│   │   └── external_brt_data.sql
│   ├── silver/               # Camada Silver - limpeza e normalização
│   │   └── consolidated_brt_data.sql
│   ├── gold/                 # Camada Gold - agregações e métricas
│   │   └── vehicles_dashboard.sql
│   └── schema.yml            # Documentação e testes de qualidade
└── tests/                    # Testes customizados adicionais

<a name="model"/>

### Camadas de modelagem

- Bronze: Dados brutos ingeridos do GCS (Google Cloud Storage) e disponibilizados no BigQuery como tabela externa.	`models/bronze/external_brt_data.sql`
- Silver:	Dados limpos, normalizados e enriquecidos.	`models/silver/consolidated_brt_data.sql`
- Gold:	Métricas e agregações prontas para consumo.	`models/gold/vehicles_dashboard.sql`

<a name="docs"/>

### Documentação e Testes

Os arquivos .yml contêm documentação detalhada de cada modelo e testes de qualidade com dbt_expectations, garantindo integridade e consistência dos dados.
As descrições são propagadas automaticamente para o BigQuery via +persist_docs.

Exemplo (trecho de models/schema.yml):
```
models:
  - name: consolidated_brt_data
    description: "Camada Silver com dados normalizados e enriquecidos do BRT."
    tests:
      - dbt_expectations.expect_table_row_count_to_be_between:
          arguments:
            min_value: 1
      - dbt_expectations.expect_column_values_to_not_be_null:
          arguments:
            column_name: codigo
```
---
<a name="setup"/>

## ⚙️ Setup do Ambiente de Desenvolvimento Local

<a name="setup1"/>

### 1. Pré-requisitos

- Instalar e ativar **Docker Desktop**
- Instalar **Python 3.10**
- Autenticar o **Google Cloud SDK** (`gcloud auth login`)
- Habilitar as APIs:
  - **Cloud Storage API**
  - **BigQuery API**

<a name="setup2"/>

### 2. Criação do ambiente virtual

```bash
python3.10 -m venv venv
source venv/bin/activate
```
<a name="setup3"/>

### 3. Instalar dependências

As versões foram fixadas para garantir compatibilidade com Prefect 1.4.1 e macOS ARM.
Instale as dependências a partir do arquivo requirements.txt:

```
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-deps
```
<a name="setup4"/>

### 4. Configuração do Docker 

Linux:
```bash
export DOCKER_HOST=unix:///var/run/docker.sock
sudo systemctl start docker
```

MacOS (Apple Silicon):
```
export DOCKER_HOST=unix://$HOME/.docker/run/docker.sock
```

Verifique se o Docker está acessível:

```
docker ps
```

Se o comando listar containers, o daemon do Docker está ativo e acessível.

Dica: adicione o comando de export DOCKER_HOST ao seu ~/.zshrc (macOS) ou ~/.bashrc (Linux)
para que a configuração seja carregada automaticamente em novos terminais.

<a name="setup5"/>

### 5. Subir o Prefect Server Local e Iniciar o server

Execute:
```
prefect backend server
```
```
prefect server start
```

Você deve ver a mensagem:
```
Visit http://localhost:8080 to get started, or check out the docs at https://docs.prefect.io
```
<a name="setup6"/>

### 6. Variáveis de ambiente e credenciais GCP

Para rodar localmente, copie o arquivo .env.example para .env e atualize os valores conforme sua configuração:
```
GCP_PROJECT=desafio-civitas-brt-ari
GCS_BUCKET=civitas-brt-data-ari
GOOGLE_APPLICATION_CREDENTIALS=/Users/<usuario>/desafio-civitas-brt-ari/prefect-gcp-access-xxxx.json
```

Caso não possua acesso ao GCP, é possível testar o pipeline apenas até a geração dos arquivos CSV locais.

#### Configuração de credenciais GCP para o DBT e Prefect

Tanto o Prefect quanto o DBT utilizam a mesma conta de serviço (Service Account)
para acessar o Google Cloud Storage (GCS) e o BigQuery.

No arquivo profiles.yml do DBT, o caminho da credencial é definido dinamicamente usando a variável de ambiente:
```
keyfile: "{{ env_var('GOOGLE_APPLICATION_CREDENTIALS') }}"
```
Isso garante segurança e portabilidade, evitando caminhos hardcoded.

Antes de rodar o DBT, carregue o .env:
```
source venv310/bin/activate
export $(grep -v '^#' .env | xargs)
```

Em seguida, execute:
```
cd dbt_project
dbt run
dbt test
```
ℹ️ Todas as variáveis de ambiente (GCP, Prefect e DBT) são centralizadas no arquivo .env para garantir segurança e facilidade de configuração.



