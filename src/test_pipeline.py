"""
Same as scheduler but smaller intervals for testing.
Executes every 30s for 2 min
"""

import pandas as pd
from scheduler import run_pipeline, upload_consolidated_to_gcs, consolidate_csv
from tasks import fetch_brt_data, save_to_csv, upload_to_gcs

if __name__ == "__main__":
    print("\n🚀 Iniciando teste rápido da pipeline (2 min, execuções a cada 30s)...")

    silver_path="data/test_silver"
    bronze_path="data/test_bronze"

    run_pipeline(interval_minutes=0.5, total_runs=4, folder=bronze_path)
    consolidated_file = consolidate_csv(silver_path, bronze_path)
    upload_consolidated_to_gcs(consolidated_file)
