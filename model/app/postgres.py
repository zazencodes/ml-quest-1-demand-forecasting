import pandas as pd
import psycopg2
from psycopg2 import sql


def run_query(
    query, fetch=True, dbname="postgres", user="postgres", host="localhost", port=5432
):
    # Connect to PostgreSQL
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port)
    cur = conn.cursor()

    # Execute the SELECT query
    cur.execute(query)

    if fetch:
        # Fetch the results
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        # Close the cursor and connection
        cur.close()
        conn.close()

        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=colnames)

        return df
    else:
        conn.commit()


def upload_to_postgres(
    df, table_name, dbname="postgres", user="postgres", host="localhost", port=5432
):
    # Connect to PostgreSQL
    conn = psycopg2.connect(dbname=dbname, user=user, host=host, port=port)
    cur = conn.cursor()

    # Create table if it doesn't exist
    create_table_query = sql.SQL(
        """
        CREATE TABLE IF NOT EXISTS {table} (
            {fields}
        )
    """
    ).format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(", ").join(
            sql.SQL("{} {}").format(
                sql.Identifier(col),
                sql.SQL(pandas_to_postgres_type(str(df[col].dtype))),
            )
            for col in df.columns
        ),
    )
    cur.execute(create_table_query)
    conn.commit()

    # Insert data into table
    for index, row in df.iterrows():
        insert_query = sql.SQL(
            """
            INSERT INTO {table} ({fields}) VALUES ({values})
        """
        ).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(", ").join(map(sql.Identifier, df.columns)),
            values=sql.SQL(", ").join(sql.Placeholder() * len(df.columns)),
        )
        cur.execute(insert_query, tuple(row))

    conn.commit()
    cur.close()
    conn.close()


def pandas_to_postgres_type(dtype):
    if dtype == "int64":
        return "INTEGER"
    elif dtype == "float64":
        return "FLOAT"
    elif dtype == "bool":
        return "BOOLEAN"
    else:
        return "TEXT"
