import streamlit as st
import pandas as pd
import altair as alt
import os

from postgres import run_postgres_query

POSTGRES_DB_ARGS = dict(
    host=os.environ["POSTGRES_HOST"],
    user=os.environ["POSTGRES_USER"],
    dbname=os.environ["POSTGRES_DB"],
    port=int(os.environ["POSTGRES_PORT"]),
)

##################################################################
##################################################################
##################################################################
##################################################################
##################################################################

# Load data
current_meal_demand_df = run_postgres_query(
    "SELECT * FROM current_meal_demand",
    **POSTGRES_DB_ARGS,
)
number_of_forecasted_weeks = current_meal_demand_df[
    current_meal_demand_df["period"] == "Future"
].week_number.nunique()
updated_date = (
    run_postgres_query(
        "SELECT updated_date FROM current_meal_demand_metadata;", **POSTGRES_DB_ARGS
    )["updated_date"]
    .astype(str)
    .tolist()[0]
)


def get_future_demand_df(current_meal_demand_df):
    """
    Gets future demand subset (next X weeks)
    """
    return current_meal_demand_df[current_meal_demand_df["period"] == "Future"]


def get_previous_demand_df(current_meal_demand_df, number_of_forecasted_weeks):
    """
    Gets previous demand subset (prev X weeks)
    """
    prev_period_weeks = (
        current_meal_demand_df[current_meal_demand_df["period"] == "Past"]
        .week_number.sort_values()
        .drop_duplicates()
        .iloc[-number_of_forecasted_weeks:]
        .tolist()
    )
    previous_demand_df = current_meal_demand_df[
        current_meal_demand_df.week_number.isin(prev_period_weeks)
    ]
    return previous_demand_df


# Prepare filtered data
future_demand_df = get_future_demand_df(current_meal_demand_df)
previous_demand_df = get_previous_demand_df(
    current_meal_demand_df, number_of_forecasted_weeks
)

##################################################################
##################################################################
##################################################################
##################################################################
##################################################################

st.title("Meal Demand Forecasting Dashboard")
soft_returns = "   "
st.markdown(
    f"""
Current predicted order demand for the kingdom.

**Date**: {updated_date}{soft_returns}
**Number of Future Weeks**: {number_of_forecasted_weeks}{soft_returns}
**Future Weeks**: {[int(week) for week in sorted(future_demand_df.week_number.unique())]}
"""
)

##################################################################
##################################################################
##################################################################
##################################################################
##################################################################

st.header("Summary", divider="gray")


def get_summary_metrics(data_subset: pd.DataFrame) -> dict:
    return dict(
        total_demand=data_subset["num_orders"].sum(),
        num_cities=data_subset["city_name"].nunique(),
        num_meals=data_subset["meal_name"].nunique(),
        highest_demand_city=data_subset.groupby("city_name")["num_orders"]
        .sum()
        .idxmax(),
        highest_demand_city_orders=data_subset.groupby("city_name")["num_orders"]
        .sum()
        .max(),
        lowest_demand_city=data_subset.groupby("city_name")["num_orders"]
        .sum()
        .idxmin(),
        lowest_demand_city_orders=data_subset.groupby("city_name")["num_orders"]
        .sum()
        .min(),
        highest_demand_meal=data_subset.groupby("meal_name")["num_orders"]
        .sum()
        .idxmax(),
        highest_demand_meal_orders=data_subset.groupby("meal_name")["num_orders"]
        .sum()
        .max(),
        lowest_demand_meal=data_subset.groupby("meal_name")["num_orders"]
        .sum()
        .idxmin(),
        lowest_demand_meal_orders=data_subset.groupby("meal_name")["num_orders"]
        .sum()
        .min(),
    )


def get_prev_pct_diff(value, previous_demand_df, filter_on=None) -> str:
    if filter_on:
        column_name = filter_on["name"]
        column_value = filter_on["value"]
        prev_subset = previous_demand_df[
            previous_demand_df[column_name] == column_value
        ]
    else:
        prev_subset = previous_demand_df
    prev_value = prev_subset.num_orders.sum()
    pct_diff = (value - prev_value) / prev_value * 100
    return f"{pct_diff:.1f}%"


# Calculate summary metrics
future_summary_metrics = get_summary_metrics(future_demand_df)  # pyright: ignore
prev_summary_metrics = get_summary_metrics(previous_demand_df)  # pyright: ignore


# Totals
col1, col2, col3 = st.columns(3)
col1.metric(
    "Total Order Demand",
    f'{future_summary_metrics["total_demand"]:,.0f}',
    get_prev_pct_diff(future_summary_metrics["total_demand"], previous_demand_df),
)
col2.metric(
    "Num Cities",
    f'{future_summary_metrics["num_cities"]:,.0f}',
)
col3.metric(
    "Num Meals",
    f'{future_summary_metrics["num_meals"]:,.0f}',
)


##################################################################
##################################################################
##################################################################
##################################################################
##################################################################


st.header("Weekly Forecasted Demand", divider="gray")

# Dropdown for city_name
city_names = list(sorted(current_meal_demand_df["city_name"].unique().tolist()))
all_cities_key = "All Cities"
selected_city = st.selectbox("Select City", [all_cities_key] + city_names)


# Dropdown for meal_name
meal_names = list(sorted(current_meal_demand_df["meal_name"].unique().tolist()))
all_meals_key = "All Meals"
selected_meal = st.selectbox("Select Meal", [all_meals_key] + meal_names)

# Filter the dataframe to get available meals for the selected city

if selected_city == all_cities_key:
    city_df_filter = pd.Series(True, index=current_meal_demand_df.index)
else:
    city_df_filter = current_meal_demand_df["city_name"] == selected_city

if selected_meal == all_meals_key:
    meal_df_filter = pd.Series(True, index=current_meal_demand_df.index)
else:
    meal_df_filter = current_meal_demand_df["meal_name"] == selected_meal

city_meal_df_filter = city_df_filter & meal_df_filter

demand_chart = (
    alt.Chart(
        current_meal_demand_df[
            ["week_number", "num_orders", "period"]
        ][  # pyright: ignore
            city_meal_df_filter
        ].rename(  # pyright: ignore
            columns={
                "week_number": "Week Number",
                "num_orders": "Number of Orders",
                "period": "Period",
            }
        )
    )
    .mark_line()
    .encode(
        x="Week Number",
        y="Number of Orders",
        color="Period",
    )
    .properties(title="Order Predictions (Aggregated)")
)
st.altair_chart(demand_chart, use_container_width=True)

future_df_filter = current_meal_demand_df["period"] == "Future"
weekly_pivot_df = (
    current_meal_demand_df[city_meal_df_filter & future_df_filter]
    .groupby(["city_name", "meal_name", "week_number"])
    .num_orders.sum()
    .unstack(level=2)
    .fillna(0)
    .astype(int)
    .reset_index()
)
st.dataframe(
    weekly_pivot_df.rename(columns={"city_name": "City", "meal_name": "Meal"}),
    hide_index=True,
)


##################################################################
##################################################################
##################################################################
##################################################################
##################################################################


st.header("Top Cities", divider="gray")

top_cities_df = (
    future_demand_df.groupby("city_name")["num_orders"]
    .sum()
    .reset_index()
    .sort_values(by="num_orders", ascending=False)
    .head(10)
)
top_cities_df["orders"] = top_cities_df.city_name.apply(
    lambda city_name: future_demand_df[future_demand_df.city_name == city_name]
    .groupby("week_number")  # pyright: ignore
    .num_orders.sum()
    .sort_index()
    .tolist()
)

st.dataframe(
    top_cities_df,
    column_config={
        "city_name": st.column_config.TextColumn("City"),
        "num_orders": st.column_config.NumberColumn(
            "Forecasted Orders",
            help=f"Total number of orders for city (next {number_of_forecasted_weeks} weeks)",
            format="%d",
        ),
        "orders": st.column_config.LineChartColumn(
            "Forecasted Orders Trend",
            help=f"Number of forecasted order for city (next {number_of_forecasted_weeks} weeks)",
            width="medium",
        ),
    },
    hide_index=True,
)


##################################################################
##################################################################
##################################################################
##################################################################
##################################################################


st.header("Top Meals", divider="gray")

top_meals_df = (
    future_demand_df.groupby("meal_name")["num_orders"]
    .sum()
    .reset_index()
    .sort_values(by="num_orders", ascending=False)
    .head(10)
)
top_meals_df["orders"] = top_meals_df.meal_name.apply(
    lambda meal_name: future_demand_df[future_demand_df.meal_name == meal_name]
    .groupby("week_number")  # pyright: ignore
    .num_orders.sum()
    .sort_index()
    .tolist()
)

st.dataframe(
    top_meals_df,
    column_config={
        "meal_name": st.column_config.TextColumn("Meal"),
        "num_orders": st.column_config.NumberColumn(
            "Forecasted Orders",
            help=f"Total number of orders for meal (next {number_of_forecasted_weeks} weeks)",
            format="%d",
        ),
        "orders": st.column_config.LineChartColumn(
            "Forecasted Orders Trend",
            help=f"Number of forecasted order for meal (next {number_of_forecasted_weeks} weeks)",
            width="medium",
        ),
    },
    hide_index=True,
)

##################################################################
##################################################################
##################################################################
##################################################################
##################################################################

st.header("Highest Demand", divider="gray")

# Highest demand city
col1, col2 = st.columns(2)
col1.metric(
    "Highest Demand City",
    future_summary_metrics["highest_demand_city"],
)
col2.metric(
    "Number of Orders",
    f'{future_summary_metrics["highest_demand_city_orders"]:,.0f}',
    get_prev_pct_diff(
        future_summary_metrics["highest_demand_city_orders"],
        previous_demand_df,
        filter_on=dict(
            name="city_name",
            value=future_summary_metrics["highest_demand_city"],
        ),
    ),
)

# Highest demand meal
col1, col2 = st.columns(2)
col1.metric(
    "Highest Demand Meal",
    future_summary_metrics["highest_demand_meal"],
)
col2.metric(
    "Number of Orders",
    f'{future_summary_metrics["highest_demand_meal_orders"]:,.0f}',
    get_prev_pct_diff(
        future_summary_metrics["highest_demand_meal_orders"],
        previous_demand_df,
        filter_on=dict(
            name="meal_name",
            value=future_summary_metrics["highest_demand_meal"],
        ),
    ),
)


##################################################################
##################################################################
##################################################################
##################################################################
##################################################################


st.header("Lowest Demand", divider="gray")

# Lowest demand city
col1, col2 = st.columns(2)
col1.metric(
    "Lowest Demand City",
    future_summary_metrics["lowest_demand_city"],
)
col2.metric(
    "Number of Orders",
    f'{future_summary_metrics["lowest_demand_city_orders"]:,.0f}',
    get_prev_pct_diff(
        future_summary_metrics["lowest_demand_city_orders"],
        previous_demand_df,
        filter_on=dict(
            name="city_name",
            value=future_summary_metrics["lowest_demand_city"],
        ),
    ),
)

# Lowest demand meal
col1, col2 = st.columns(2)
col1.metric(
    "Lowest Demand Meal",
    future_summary_metrics["lowest_demand_meal"],
)
col2.metric(
    "Number of Orders",
    f'{future_summary_metrics["lowest_demand_meal_orders"]:,.0f}',
    get_prev_pct_diff(
        future_summary_metrics["lowest_demand_meal_orders"],
        previous_demand_df,
        filter_on=dict(
            name="meal_name",
            value=future_summary_metrics["lowest_demand_meal"],
        ),
    ),
)


##################################################################
##################################################################
##################################################################
##################################################################
##################################################################


# Demand Distribution Heatmap
st.header("Demand Distribution", divider="gray")

meal_order = (
    future_demand_df.groupby("meal_name")
    .num_orders.sum()
    .sort_values(ascending=False)
    .index.tolist()
)
city_order = (
    future_demand_df.groupby("city_name")
    .num_orders.sum()
    .sort_values(ascending=False)
    .index.tolist()
)
heatmap_chart = (
    alt.Chart(
        future_demand_df.groupby(["city_name", "meal_name"])["num_orders"]
        .sum()
        .reset_index()
    )
    .mark_rect()
    .encode(
        x=alt.X("meal_name:O", sort=meal_order, title="Meal"),
        y=alt.X("city_name:O", sort=city_order, title="City"),
        color="num_orders:Q",
        tooltip=["city_name", "meal_name", "num_orders"],
    )
    .properties(title="City Meal Heatmap")
    .interactive()
)
st.altair_chart(heatmap_chart, use_container_width=True)
