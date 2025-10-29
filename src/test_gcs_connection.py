import os
from google.cloud import storage
from prefect import task, Flow
from dotenv import load_dotenv

# Carrega variáveis de ambiente (.env)
load_dotenv()

GCS_BUCKET = os.getenv("GCS_BUCKET")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

@task
def test_gcs_upload():
    print("Iniciando teste de conexão com o GCS...")
    print(f"Usando credenciais: {GOOGLE_APPLICATION_CREDENTIALS}")

    client = storage.Client()  # usa GOOGLE_APPLICATION_CREDENTIALS automaticamente
    bucket = client.bucket(GCS_BUCKET)

    test_content = "Teste de upload Prefect"
    blob = bucket.blob("test_prefect_upload.txt")
    blob.upload_from_string(test_content)

    print(f"✅ Upload bem-sucedido para gs://{GCS_BUCKET}/test_prefect_upload.txt")

with Flow("test-gcs-connection") as flow:
    test_gcs_upload()

if __name__ == "__main__":
    flow.run()