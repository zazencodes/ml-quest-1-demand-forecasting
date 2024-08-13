from ..utils.common import get_logger
from ..domain.config import Config
from tqdm import tqdm
import re

from joblib import load
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

logger = get_logger()


def predict(
    df: pd.DataFrame,
    df_final_week: pd.DataFrame,
    config: Config,
) -> pd.DataFrame:
    """
    Predict with a stack of models and return forecast.
    """
    logger.info(f"Started predict")
    df_preds = _predict_demand(df_final_week, config)
    df_forecast = _merge_df_preds_with_historical(df, df_final_week, df_preds)
    df_forecast = _inverse_encoding(df_forecast, config)

    logger.info(df_forecast)
    logger.info(df_forecast.columns)
    logger.info(df_forecast.dtypes)

    logger.info(f"Completed predict")
    return df_forecast


def _predict_demand(df_week_x, config, future_weeks=12):
    y_preds = []
    city_ids = df_week_x.city_id.values
    meal_ids = df_week_x.meal_id.values
    meal_infos = df_week_x[
        [
            "Meat",
            "Other",
            "Seafood",
            "Vegetarian",
            "beverage",
            "dessert",
            "main",
            "side",
            "starter",
        ]
    ].values.tolist()

    X_pred = df_week_x.drop(columns=["next_week_num_orders"])
    initial_week_number = int(df_week_x.week_number.max())
    for future_week_offset in tqdm(list(range(1, future_weeks + 1))):
        # 1, 2, 3, ... 12
        pred_week_num = initial_week_number + future_week_offset
        print(f"Predicting for week {pred_week_num}")
        model = _load_model(
            f"boosted_tree_stack_week_{future_week_offset}",
            artifacts_path=config.artifacts_path,
        )
        y_pred = model.predict(X_pred)
        y_preds.extend(
            [
                {
                    "period": "Future",
                    "week_number": pred_week_num,
                    "num_orders": y,
                    "city_id": city_id,
                    "meal_id": meal_id,
                    "meal_info": meal_info,
                }
                for y, city_id, meal_id, meal_info in zip(
                    y_pred, city_ids, meal_ids, meal_infos
                )
            ]
        )

    df_preds = pd.DataFrame(y_preds)
    return df_preds


def _load_model(model_name, artifacts_path):
    logger.info(f"Loading model {model_name}")
    with open(artifacts_path / f"{model_name}.pkl", "rb") as f:
        model = load(f)
    logger.info(model)
    return model


def _merge_df_preds_with_historical(
    df_past_, df_final_week_, df_future_
) -> pd.DataFrame:
    columns = ["week_number", "num_orders", "city_id", "meal_id", "meal_info", "period"]

    df_past = df_past_.copy()
    df_final_week = df_final_week_.copy()
    df_future = df_future_.copy()

    df_past["period"] = "Past"
    df_past["meal_info"] = [
        list(item)
        for item in df_past[
            [
                "Meat",
                "Other",
                "Seafood",
                "Vegetarian",
                "beverage",
                "dessert",
                "main",
                "side",
                "starter",
            ]
        ].values
    ]

    df_final_week["period"] = "Past"
    df_final_week["meal_info"] = [
        list(item)
        for item in df_final_week[
            [
                "Meat",
                "Other",
                "Seafood",
                "Vegetarian",
                "beverage",
                "dessert",
                "main",
                "side",
                "starter",
            ]
        ].values
    ]

    df_forecast = pd.concat(
        (df_past[columns], df_final_week[columns], df_future[columns]),
        axis=0,
        ignore_index=True,
    )
    return df_forecast


def _inverse_encoding(df_forecast, config) -> pd.DataFrame:
    encoders = _load_encoders(config.artifacts_path)
    df_forecast["city_name"] = encoders["city_name"].inverse_transform(
        df_forecast.city_id
    )
    df_forecast["meal_name"] = encoders["meal_name"].inverse_transform(
        df_forecast.meal_id
    )
    ohe_data = pd.DataFrame(df_forecast.meal_info.tolist())
    df_forecast[["meal_category", "meal_type"]] = (
        encoders["meal_info"].inverse_transform(ohe_data).tolist()
    )
    df_forecast = df_forecast.drop(columns=["city_id", "meal_id", "meal_info"])
    return df_forecast


def _load_encoders(artifacts_path):
    encoders = {}
    for file_path in artifacts_path.glob("*encoder.pkl"):
        with open(file_path, "rb") as f:
            encoders[re.findall(r"(.*)_encoder", file_path.name)[0]] = load(f)
    return encoders
