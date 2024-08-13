from ..utils.common import get_logger
from ..domain.config import Config
from joblib import dump
from tqdm import tqdm

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

logger = get_logger()


def train(
    df: pd.DataFrame,
    config: Config,
):
    """
    Train a stack of models and save to disk.
    """
    logger.info(f"Started train")
    _train_stack(df, config)
    logger.info(f"Completed train")


def _train_stack(df, config):
    df_i = pd.DataFrame()
    num_future_weeks = 12
    for future_week_num in tqdm(list(range(1, num_future_weeks + 1))):

        if future_week_num == 1:
            df_i = df.rename(
                columns={"next_week_num_orders": "target_num_orders"}
            ).copy()

        else:
            # Shift target (predict for following week)
            df_i["target_num_orders"] = (
                df_i.sort_values("week_number", ascending=True)
                .groupby(["city_id", "meal_id"])
                .target_num_orders.shift(-1)
            )
            df_i = df_i.dropna().copy()

        logger.info(f"week_num={future_week_num}")
        logger.info(f"len(df)={int(len(df_i))}")
        logger.info(f"max_week={int(df_i.week_number.max())}")

        X = df_i.drop(columns="target_num_orders")
        y = df_i["target_num_orders"]
        model = GradientBoostingRegressor(**vars(config.model_params))

        model.fit(X, y)

        _store_model(
            f"boosted_tree_stack_week_{future_week_num}",
            model,
            config.artifacts_path,
        )


def _store_model(model_name, model, artifacts_path):
    artifacts_path.mkdir(exist_ok=True, parents=True)
    fname = artifacts_path / f"{model_name}.pkl"
    logger.info(f"Writing model {model} to {fname}")
    with open(fname, "wb") as f:
        dump(model, f)
