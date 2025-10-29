import glob
import os
import time
import pandas as pd
from datetime import datetime
from flow import flow
from tasks import upload_to_gcs

def run_pipeline(interval_minutes=1, total_runs=10, folder="data/bronze"):
    """
    Executa o flow Prefect em intervalos fixos (default: 10 execuções, 1/minuto).
    Cada execução salva o arquivo localmente e faz upload para o GCS (camada Bronze).
    """
    print(f"\n⏱️ Iniciando scheduler: {total_runs} execuções a cada {interval_minutes} minuto(s).")

    for i in range(total_runs):
        print(f"\n🚀 Execução {i+1}/{total_runs} — {datetime.now().strftime('%H:%M:%S')}")
        try:
            flow.run(parameters={"folder": folder})
        except Exception as e:
            print(f"\n❌ Erro na execução {i+1}: {e}")
        if i < total_runs - 1:
            time.sleep(interval_minutes * 60)

    print("\n✅ Scheduler finalizado. Consolidando arquivos...")


def consolidate_csv(silver_path="data/silver", bronze_path="data/bronze"):
    """
    Consolida os arquivos CSV gerados em um único arquivo (camada Silver).
    """
    os.makedirs(silver_path, exist_ok=True)
    files = sorted(glob.glob(f"{bronze_path}/brt_*.csv"))

    if not files:
        print("⚠️ Nenhum arquivo encontrado para consolidação.")
        return None

    df_all = pd.concat([pd.read_csv(f) for f in files])
    consolidated_filename = f"{silver_path}/brt_consolidado_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
    df_all.to_csv(consolidated_filename, index=False)
    print(f"📦 Arquivo consolidado criado: {consolidated_filename}")
    return consolidated_filename


def upload_consolidated_to_gcs(consolidated_filename):
    """
    Faz upload do CSV consolidado para o bucket GCS (camada Silver).
    """
    if not consolidated_filename:
        print("⚠️ Nenhum arquivo consolidado encontrado para upload.")
        return

    print("☁️ Enviando arquivo consolidado para GCS (Silver Layer)...")
    try:
        # Executa task Prefect fora de um Flow (Prefect 1.x usa .run())
        upload_to_gcs.run(consolidated_filename, layer="silver")
        print("✅ Upload da camada Silver concluído com sucesso.")
    except Exception as e:
        print(f"❌ Falha ao enviar arquivo consolidado: {e}")


if __name__ == "__main__":
    run_pipeline(interval_minutes=1, total_runs=10)
    consolidated_file = consolidate_csv()
    upload_consolidated_to_gcs(consolidated_file)