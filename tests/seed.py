from sqlitecursor import SqliteCursor
import os

DBNAME = "test.db"
DBPATH = os.path.join(os.path.dirname(__file__), DBNAME)


def seed(dbpath=DBPATH):
    with SqliteCursor(dbpath) as cur:
        SQL = """ DELETE FROM test_table; """
        cur.execute(SQL)

        SQL = """ INSERT INTO test_table (field) VALUES (?); """
        vals = [('A', ), ('B', ), ('C', )]
        for val in vals:
            cur.execute(SQL, val)


if __name__ == "__main__":
    seed()
