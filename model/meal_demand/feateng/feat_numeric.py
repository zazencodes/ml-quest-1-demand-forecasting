from numpy._core.defchararray import encode
from sklearn.preprocessing import StandardScaler
from ..utils.common import get_logger
from ..domain.config import Config
from joblib import dump
from joblib import load
import pandas as pd
import re

logger = get_logger()


def feat_numeric(
    df: pd.DataFrame, config: Config, fit_new_encoders: bool = False
) -> pd.DataFrame:
    """
    Encodes numeric features.
    """
    logger.info("Started feateng: step=numeric")
    if fit_new_encoders:
        encoders = {}
        encoders["price_scaler"] = StandardScaler()

    else:
        encoders = _load_encoders(config)

    logger.info(encoders)
    df = _apply_scaling(df, encoders["price_scaler"], fit_new_encoders)
    df = _add_price_features(df)

    if fit_new_encoders:
        _store_encoders(config, encoders)

    logger.info("Completed feateng: step=numeric")
    return df


def _load_encoders(config: Config) -> dict:
    encoders = {}
    for file_path in config.artifacts_path.glob("*encoder.pkl"):
        with open(file_path, "rb") as f:
            encoders[re.findall(r"(.*)_encoder", file_path.name)[0]] = load(f)
    return encoders


def _store_encoders(config: Config, encoders: dict):
    config.artifacts_path.mkdir(exist_ok=True, parents=True)
    for name, obj in encoders.items():
        with open(config.artifacts_path / f"{name}_encoder.pkl", "wb") as f:
            dump(obj, f)


def _apply_scaling(df, price_scaler, fit_new_encoders):
    if fit_new_encoders:
        df["base_price_normed"] = price_scaler.fit_transform(
            df.base_price.values.reshape(-1, 1)
        )
        df["checkout_price_normed"] = price_scaler.transform(
            df.checkout_price.values.reshape(-1, 1)
        )
    else:
        df["base_price_normed"] = price_scaler.transform(
            df.base_price.values.reshape(-1, 1)
        )
        df["checkout_price_normed"] = price_scaler.transform(
            df.checkout_price.values.reshape(-1, 1)
        )
    df = df.drop(columns=["base_price", "checkout_price"])
    return df


def _add_price_features(df):
    df["price_diff"] = df.base_price_normed - df.checkout_price_normed
    return df
