from ..utils.common import get_logger
from ..domain.config import Config
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

logger = get_logger()


def feat_encode(df: pd.DataFrame, config: Config) -> tuple[pd.DataFrame, list[str]]:
    """
    Encodes categorical features.
    """
    logger.info("Started feateng: step=encode")
    # encoders = _load_encoders(config)
    # df, encoded_features = _add_encoded_feature(df, "", encoders)
    logger.info("Completed feateng: step=encode")
    # return df, encoded_features


# def _add_encoded_feature(
#     df: pd.DataFrame,
#     feature_column: str,
#     encoder: OneHotEncoder,
# ) -> tuple[pd.DataFrame, lsit[str]]:
#     X_ohe = ohe.transform(df[[feature_column]])
#     ohe_cols = [f"{feature_column}_ohe_{i}" for i in range(X_ohe.shape[1])]
#     ohe_df = pd.DataFrame(X_ohe.toarray(), dtype=int, columns=cols)
#     df = pd.concat((df, ohe_df), axis=1)
#     return df, ohe_cols


def _load_encoders(config: Config):
    pass
