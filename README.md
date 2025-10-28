# 🚍 Desafio de Data Engineer - Civitas

Este repositório contém a implementação do desafio técnico para a vaga de **Engenheiro(a) de Dados** na [Civitas](https://civitas.rio/).  
O objetivo é construir uma **pipeline ELT em arquitetura Medallion (Bronze → Silver → Gold)**,  
utilizando **Prefect 1.4.1** e **Google Cloud (GCS + BigQuery)** para ingestão, armazenamento e transformação de dados do BRT em tempo real.


---

## ⚙️ Ambiente e Ferramentas

| Componente | Versão | Função |
|-------------|---------|--------|
| **Python** | 3.10 | Linguagem principal |
| **Prefect** | 1.4.1 | Orquestração da pipeline |
| **Docker / Docker Compose** | 4.4.4 / 1.29.2 | Infraestrutura local e agente |
| **Google Cloud SDK** | latest | Armazenamento e consultas |
| **DBT (BigQuery Adapter)** | latest | Modelagem das camadas Silver/Gold |

---

## ⚙️ Setup do Ambiente Local

### 1. Pré-requisitos

- Docker Desktop (rodando)
- Python 3.10
- Google Cloud SDK (autenticado)
- Conta BigQuery (habilitada)

---

###⃣ 2. rCiação do ambiente virtual

```bash
python3.10 -m venv venv
source venv/bin/activate

---

### 3. Instalar dependências

As versões foram fixadas para garantir compatibilidade com Prefect 1.4.1 e macOS ARM.
Instale as dependências a partir do arquivo requirements.txt:

`pip install --upgrade pip setuptools wheel`
`pip install -r requirements.txt`

---

### 4. Configuração do Docker 

Para Linux

O Prefect se conecta diretamente ao daemon do Docker via socket padrão do Linux:
`export DOCKER_HOST=unix:///var/run/docker.sock`
Verifique se o daemon está ativo:

`sudo systemctl status docker`

Caso não esteja, inicie com:
`sudo systemctl start docker`

Para macOS (Apple Silicon)

Defina o caminho correto para o Docker:

`export DOCKER_HOST=unix://$HOME/.docker/run/docker.sock`

Ambos Linux e macOS:
Verifique se o Docker está acessível:

`docker ps`

Se o comando listar containers, o daemon do Docker está ativo e acessível ✅.

💡 Dica: adicione o comando de export DOCKER_HOST ao seu ~/.zshrc (macOS) ou ~/.bashrc (Linux)
para que a configuração seja carregada automaticamente em novos terminais.
---

### 5. Subir o Prefect Server Local e Iniciar o server
`prefect backend server`
`prefect server start`

---
### 6. Testar que ambiente foi criado
Visit http://localhost:8080 to get started, or check out the docs at https://docs.prefect.io


