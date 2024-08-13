from ..utils.common import get_logger
from ..domain.config import Config

import pandas as pd

logger = get_logger()


def prep_load(config: Config):
    """
    Loads data for prediction or training.
    """
    logger.info("Started dataprep: step=load")
    df = _load(config)
    df = _clean(df)
    logger.info("Completed dataprep: step=load")
    return df


def _load(config: Config) -> pd.DataFrame:
    fpath = config.data_path / "meal_demand_historical.csv"
    df_train_raw = pd.read_csv(fpath)
    logger.info(f"Loaded data: path={fpath};len={len(df_train_raw)}")
    return df_train_raw


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    df = _parse_num_orders(df)
    df = _clean_num_orders(df)
    df = _remove_low_temporal_coverage(df)

    return df


def _parse_num_orders(df: pd.DataFrame):
    print(f"Length before parsing num_orders: {len(df)}")

    df["num_orders"] = df["num_orders"].fillna("").str.replace(",", "")
    null_orders = df["num_orders"] == ""
    df = df[~null_orders].copy()
    df["num_orders"] = pd.to_numeric(df["num_orders"])

    print(f"Length after parsing num_orders:  {len(df)}")
    return df


def _clean_num_orders(df: pd.DataFrame):
    print(f"Length before cleaning num_orders: {len(df)}")

    max_num_orders = 6.902760e03
    negative_orders = df.num_orders < 0
    zero_orders = df.num_orders == 0
    huge_orders = df.num_orders > max_num_orders
    df = df[~(negative_orders | zero_orders | huge_orders)].copy()

    print(f"Length after cleaning num_orders:  {len(df)}")
    return df


def _remove_low_temporal_coverage(df: pd.DataFrame):
    print(f"Length before removing low temporal coverage records: {len(df)}")
    df = df[~df.city_name.isin(("Osprey Point",))].copy()
    print(f"Length after removing low temporal coverage records:  {len(df)}")
    return df
