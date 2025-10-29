from prefect import Flow
from tasks import fetch_brt_data, save_to_csv, upload_to_gcs

with Flow("brt-data-pipeline") as flow:
    data = fetch_brt_data()
    csv_file = save_to_csv(data)
    gcs_path = upload_to_gcs(csv_file)

if __name__ == "__main__":
    print("\n 🚀 Executando flow Prefect localmente...")
    flow.run()