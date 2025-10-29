import os
import requests
import pandas as pd
from datetime import datetime
from prefect import task
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "https://dados.mobilidade.rio/gps/brt")
GCS_BUCKET = os.getenv("GCS_BUCKET", "civitas-brt-data")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

@task
def fetch_brt_data():
    """
        Faz requisição à API do BRT e retorna os dados em formato JSON.
    """

    print(f"\n 🔄 Consultando API do BRT: {API_URL}")
    resp = requests.get(API_URL, timeout=15)

    if resp.status_code != 200:
        raise Exception(f"Erro ao consultar API: {resp.status_code}")
    

    # O retorno é JSON e contém a chave 'veiculos'
    data = resp.json()
    if "veiculos" not in data:
        raise ValueError("Resposta inesperada da API: chave 'veiculos' não encontrada.")

    veiculos = data["veiculos"]

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    for v in veiculos:
        v["captured_at"] = timestamp

    print(f"✅ Capturados {len(veiculos)} registros às {timestamp}")
    return veiculos

@task
def save_to_csv(data):
    """
    Salva os dados capturados em um arquivo CSV local (camada Bronze).
    """
    
    os.makedirs("data", exist_ok=True)
    filename = f"data/brt_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    
    print(f"\n 💾 Dados salvos localmente em {filename}")
    return filename

@task
def upload_to_gcs(filename):
    """
    Faz upload do arquivo CSV para o bucket GCS configurado.
    """

    print(f"\n ☁️ Iniciando upload para o GCS ({GCS_BUCKET})...")
    client = storage.Client()  # usa GOOGLE_APPLICATION_CREDENTIALS automaticamente
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(f"bronze/{os.path.basename(filename)}")
    blob.upload_from_filename(filename)
    
    print(f"\n ✅ Upload concluído: gs://{GCS_BUCKET}/bronze/{os.path.basename(filename)}")
    return f"gs://{GCS_BUCKET}/bronze/{os.path.basename(filename)}"
