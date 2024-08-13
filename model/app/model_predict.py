from meal_demand.dataprep.prep_load import prep_load
from meal_demand.feateng.feat_encode import feat_encode
from meal_demand.feateng.feat_numeric import feat_numeric
from meal_demand.feateng.feat_ts import feat_ts
from meal_demand.ml.predict import predict
from meal_demand.domain.config import Config
from pathlib import Path
import pandas as pd
import os
from datetime import datetime

from postgres import upload_to_postgres, run_query

db_args = dict(
    host=os.getenv("POSTGRES_HOST"),
    user=os.getenv("POSTGRES_USER"),
    dbname=os.getenv("POSTGRES_DB"),
    port=int(os.getenv("POSTGRES_PORT", "5432")),
)
if not all(list(db_args.values())):
    raise ValueError("Postgres environment not setup")


def generate_forecast():
    config = Config(
        data_path=Path("/data"),
        artifacts_path=Path("/artifacts"),
    )
    df = prep_load(config)
    df = feat_encode(df, config, fit_new_encoders=False)
    df = feat_numeric(df, config, fit_new_encoders=False)
    df, df_final_week = feat_ts(df)
    df_forecast = predict(df, df_final_week, config)
    _store_forecast(df_forecast)


def _store_forecast(df_forecast: pd.DataFrame):
    table_name = "current_meal_demand"

    print(
        f"Replacing {table_name} with {len(df_forecast)} rows of fresh forecast predictions"
    )
    run_query(
        f"DROP TABLE IF EXISTS {table_name}",
        fetch=False,
        **db_args,  # pyright: ignore
    )
    upload_to_postgres(
        df_forecast,
        table_name=table_name,
        **db_args,  # pyright: ignore
    )
    run_query(
        f"""
    CREATE TABLE IF NOT EXISTS current_meal_demand_metadata (
        updated_date date
    );
    DELETE FROM current_meal_demand_metadata WHERE true;
    INSERT INTO current_meal_demand_metadata values ('{datetime.now().date().isoformat()}');
    """,
        fetch=False,
        **db_args,  # pyright: ignore
    )
