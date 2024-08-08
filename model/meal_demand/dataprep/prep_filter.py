from ..utils.common import get_logger
import pandas as pd


logger = get_logger()


def prep_filter(df: pd.DataFrame):
    """
    Filters data for prediction or training.
    """
    logger.info("Started dataprep: step=filter")
    df = _example_filter(df)
    logger.info("Completed dataprep: step=filter")
    return df


def _example_filter(df: pd.DataFrame) -> pd.DataFrame:
    # logger.info(f"Droped {len_diff} rows ({len_diff/len_0*100:.1f}%)")
    # return df
    pass
