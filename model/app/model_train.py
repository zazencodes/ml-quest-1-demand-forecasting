from meal_demand.dataprep.prep_load import prep_load
from meal_demand.feateng.feat_encode import feat_encode
from meal_demand.feateng.feat_numeric import feat_numeric
from meal_demand.feateng.feat_ts import feat_ts
from meal_demand.ml.train import train
from meal_demand.domain.config import Config, ModelHyperparams
from pathlib import Path


def train_models():
    config = Config(
        data_path=Path("/data"),
        artifacts_path=Path("/artifacts"),
        model_params=ModelHyperparams(
            learning_rate=0.05,
            max_depth=5,
            min_samples_split=10,
            n_estimators=100,
            subsample=0.8,
        ),
    )
    if config.model_params is None:
        raise ValueError("Must set config hyperparameters")
    df = prep_load(config)
    df = feat_encode(df, config, fit_new_encoders=True)
    df = feat_numeric(df, config, fit_new_encoders=True)
    df, _ = feat_ts(df)
    train(df, config)
