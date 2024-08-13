from ..utils.common import get_logger
import pandas as pd

logger = get_logger()


def feat_ts(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Feature engineer timeseries variables.
    """
    logger.info("Started feateng: step=ts")
    df = _add_calendar_features(df)
    df, df_final_week = _add_ts_features(df)
    logger.info("Completed feateng: step=ts")
    return df, df_final_week


def _apply_yearly_offset_by_month(month_num):
    if month_num <= 12:
        return month_num
    elif month_num <= 24:
        return month_num - 12
    elif month_num <= 36:
        return month_num - 24
    else:
        raise NotImplementedError(month_num)


def _apply_yearly_offset_by_quarter(querter_num):
    if querter_num <= 4:
        return querter_num
    elif querter_num <= 8:
        return querter_num - 4
    elif querter_num <= 12:
        return querter_num - 8
    else:
        raise NotImplementedError(querter_num)


def _add_calendar_features(df):
    logger.info("Adding calendar features")
    df["month_num"] = (df.week_number // (52 / 12)).astype(int).apply(
        _apply_yearly_offset_by_month
    ) + 1
    df["quarter_num"] = (df.week_number // (52 / 4)).astype(int).apply(
        _apply_yearly_offset_by_quarter
    ) + 1
    df["year_num"] = (df.week_number // 52).astype(int) + 1
    logger.info("Done adding calendar features")
    return df


def _add_ts_features(df_: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df_.copy()

    logger.info("Adding rolling features")

    g = ["city_id", "meal_id"]

    # Shift target (predict for next week)
    df["next_week_num_orders"] = df.groupby(g).num_orders.shift(-1).fillna(0)

    # Num next week orders from last year
    df["num_orders_last_year"] = df.groupby(g).next_week_num_orders.shift(52).fillna(0)

    # Num orders from past week
    df["num_orders_last_week"] = df.groupby(g).num_orders.shift(1).fillna(0)

    # Num orders rolling average past 4 weeks
    df["num_orders_rolling_4_weeks"] = (
        df.groupby(g)
        .next_week_num_orders.rolling(4)
        .mean()
        .reset_index()
        .sort_values("level_2")
        .drop(columns=g)
        .set_index("level_2")
        .next_week_num_orders.fillna(0)
    )

    # Num orders rolling average past 16 weeks
    df["num_orders_rolling_16_weeks"] = (
        df.groupby(g)
        .next_week_num_orders.rolling(16)
        .mean()
        .reset_index()
        .sort_values("level_2")
        .drop(columns=g)
        .set_index("level_2")
        .next_week_num_orders.fillna(0)
    )

    # Num order rolling averages from same week last year
    df["num_orders_last_year_rolling_4_weeks"] = (
        df.groupby(g).num_orders_rolling_4_weeks.shift(52).fillna(0)
    )
    df["num_orders_last_year_rolling_16_weeks"] = (
        df.groupby(g).num_orders_rolling_16_weeks.shift(52).fillna(0)
    )

    # Drop first year and last week
    df_final_week = df[df.week_number == 145].copy()
    df = df[(df.week_number > 52) & (df.week_number != 145)].copy()

    logger.info("Done adding rolling features")
    return df, df_final_week  # pyright: ignore
