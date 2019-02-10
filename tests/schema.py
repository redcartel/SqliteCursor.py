from sqlitecursor import SqliteCursor
import os

DBNAME = "test.db"
DBPATH = os.path.join(os.path.dirname(__file__), DBNAME)


def schema(dbpath=DBPATH):
    with SqliteCursor(dbpath) as cur:
        SQL = "DROP TABLE IF EXISTS test_table;"
        cur.execute(SQL)
        SQL = """ CREATE TABLE test_table(
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            field TEXT
            ); """
        cur.execute(SQL)


if __name__ == "__main__":
    schema()
