from ..utils.common import get_logger
from ..domain.config import Config
import pandas as pd

import re
from joblib import load, dump
from sklearn.preprocessing import OneHotEncoder

from .ordered_category_encoder import OrderedCategoryEncoder

import __main__

setattr(__main__, "OrderedCategoryEncoder", OrderedCategoryEncoder)

logger = get_logger()


def feat_encode(
    df: pd.DataFrame, config: Config, fit_new_encoders: bool = False
) -> pd.DataFrame:
    """
    Encodes categorical features.
    """
    logger.info("Started feateng: step=encode")
    if fit_new_encoders:
        encoders = {}
        encoders["meal_info"] = OneHotEncoder()
        encoders["city_name"] = OrderedCategoryEncoder()
        encoders["meal_name"] = OrderedCategoryEncoder()

    else:
        encoders = _load_encoders(config)

    logger.info(encoders)
    df = _add_encoded_feature(df, encoders, fit_new_encoders)

    if fit_new_encoders:
        _store_encoders(config, encoders)

    logger.info("Completed feateng: step=encode")
    return df
    # return df, encoded_features


def _add_encoded_feature(df, encoders, fit_new_encoders) -> pd.DataFrame:
    df = _apply_ohe_encoding(df, encoders["meal_info"], fit_new_encoders)
    df = _apply_ordinal_encoding(
        df,
        encoders["city_name"],
        encoders["meal_name"],
        fit_new_encoders,
    )
    return df


def _get_ohe_columns(ohe_encoder):
    columns = []
    for cols in ohe_encoder.categories_:
        columns.extend(list(cols))
    return columns


def _apply_ohe_encoding(df, meal_info_ohe, fit_new_encoders):
    logger.info("Applying one-hot-encoding to meal_category and meal_type")
    if fit_new_encoders:
        ohe_vals = meal_info_ohe.fit_transform(
            df[["meal_category", "meal_type"]].values
        ).toarray()
    else:
        ohe_vals = meal_info_ohe.transform(
            df[["meal_category", "meal_type"]].values
        ).toarray()
    df_ohe = pd.DataFrame(ohe_vals, columns=_get_ohe_columns(meal_info_ohe)).astype(int)
    df = pd.concat((df.reset_index(drop=True), df_ohe.reset_index(drop=True)), axis=1)
    df = df.drop(columns=["meal_category", "meal_type"])
    return df


def _apply_ordinal_encoding(df, city_name_encoder, meal_name_encoder, fit_new_encoders):
    logger.info("Applying ordered categorical encoding to city_name")
    ordered_city_names = (
        df.groupby("city_name")
        .num_orders.sum()
        .sort_values()
        .reset_index("city_name")
        .drop(columns="num_orders")
        .reset_index()
        .set_index("city_name")
        .to_dict()["index"]
    )
    if fit_new_encoders:
        city_name_encoder.fit(ordered_city_names)
    df["city_id"] = city_name_encoder.transform(df.city_name.values)

    logger.info("Applying ordered categorical encoding to meal_name")
    ordered_meal_names = (
        df.groupby("meal_name")
        .num_orders.sum()
        .sort_values()
        .reset_index("meal_name")
        .drop(columns="num_orders")
        .reset_index()
        .set_index("meal_name")
        .to_dict()["index"]
    )
    if fit_new_encoders:
        meal_name_encoder.fit(ordered_meal_names)
    df["meal_id"] = meal_name_encoder.transform(df.meal_name.values)

    df = df.drop(columns=["city_name", "meal_name"])

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
