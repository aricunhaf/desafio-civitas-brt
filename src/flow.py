from prefect import Flow, Parameter
from tasks import fetch_brt_data, save_to_csv, upload_to_gcs

with Flow("brt-data-pipeline") as flow:
    folder = Parameter("folder", default="data/bronze") 

    data = fetch_brt_data()
    csv_file = save_to_csv(data, folder=folder)
    gcs_path = upload_to_gcs(csv_file, layer="bronze")

if __name__ == "__main__":
    print("\n 🚀 Executando flow Prefect localmente...")
    flow.run(parameters={"folder": "data/bronze"})