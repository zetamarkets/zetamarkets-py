from psycopg_pool import ConnectionPool

pool = ConnectionPool(conninfo="dbname=zeta user=postgres password=postgres host=localhost port=5432")
