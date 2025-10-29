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
GCS_ENV = os.getenv("GCS_ENV", "dev")

@task
def fetch_brt_data():
    """
    Faz requisição à API do BRT e retorna os dados em formato JSON.
    """

    print(f"\n🔄 Consultando API do BRT: {API_URL}")
    resp = requests.get(API_URL, timeout=15)

    if resp.status_code != 200:
        raise Exception(f"❌Erro ao consultar API: {resp.status_code}")
    

    # O retorno é JSON e contém a chave 'veiculos'
    data = resp.json()
    if "veiculos" not in data:
        raise ValueError("❌Resposta inesperada da API: chave 'veiculos' não encontrada.")

    veiculos = data["veiculos"]
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    for v in veiculos:
        v["captured_at"] = timestamp

    print(f"\n✅ Capturados {len(veiculos)} registros às {timestamp}")
    return veiculos

@task
def save_to_csv(data, folder="data/bronze"):
    """
    Salva os dados capturados em um arquivo CSV local (camada Bronze).
    """
    
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/brt_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    df = pd.DataFrame(data).to_csv(filename, index=False)
    
    print(f"\n💾 Dados salvos localmente em {filename}")
    return filename

@task
def upload_to_gcs(filename, folder="prod/bronze",layer="bronze"):
    """
    Faz upload do arquivo CSV para o bucket GCS configurado.
    - `layer`: camada de destino (bronze, silver, etc).
    """
    if layer not in {"bronze", "silver", "gold"}:
        raise ValueError("Camada inválida. Use 'bronze', 'silver' ou 'gold'.")

    print(f"\n☁️ Upload para GCS ({GCS_BUCKET}) na camada '{layer}'...")
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    blob_name = f"{GCS_ENV}/{layer}/{os.path.basename(filename)}"
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(filename)

    print(f"✅ Enviado: gs://{GCS_BUCKET}/{blob_name}")
    return blob_name
