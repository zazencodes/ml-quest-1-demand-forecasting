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
    logger.info("Completed dataprep: step=load")
    return df


def _load(config: Config) -> Dict[str, pd.DataFrame]:
    # fpath = config.data_path /
    # df_train_raw = pd.read_csv(fpath)
    # logger.info(f"Loaded data: path={fpath};len={len(df_train_raw)}")
    # return df_train_raw
    pass
