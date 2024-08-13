from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from datetime import datetime
from postgres import run_postgres_query


POSTGRES_DB_ARGS = dict(
    host=os.environ["POSTGRES_HOST"],
    user=os.environ["POSTGRES_USER"],
    dbname=os.environ["POSTGRES_DB"],
    port=int(os.environ["POSTGRES_PORT"]),
)


app = FastAPI()


class ForecastRequest(BaseModel):
    city_name: str
    meal_name: str


@app.post("/forecast")
def fetch_forecast(request: ForecastRequest):
    try:
        forecast_df = run_postgres_query(
            f"""
        SELECT *
        FROM current_meal_demand
        WHERE
            city_name = '{request.city_name}'
            and meal_name = '{request.meal_name}'
        """,
            **POSTGRES_DB_ARGS,
        )
        forecast = forecast_df.to_dict(orient="records")
        return {
            "request": {
                "city_name": request.city_name,
                "meal_name": request.meal_name,
                "date": datetime.now().isoformat(),
            },
            "result": forecast,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
