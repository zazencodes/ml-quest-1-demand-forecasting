import psycopg2
import pandas as pd


def run_postgres_query(
    query,
    dbname="postgres",
    user="postgres",
    host="localhost",
    port=5432,
):
    # Connect to PostgreSQL
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port)
    cur = conn.cursor()

    # Execute the SELECT query
    cur.execute(query)

    # Fetch the results
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]  # pyright: ignore

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=colnames)  # pyright: ignore

    return df
