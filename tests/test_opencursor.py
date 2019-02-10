import unittest
from sqlitecursor import SqliteCursor, HaltCommits
from tests.schema import schema
from tests.seed import seed
import os

DBNAME = "test.db"
FILEPATH = os.path.dirname(__file__)
DBPATH = os.path.join(FILEPATH, DBNAME)


class SuccessTest(unittest.TestCase):
    def setUp(self):
        schema(DBPATH)
        seed(DBPATH)

    def tearDown(self):
        os.remove(DBPATH)

    def add_one(self):
        with SqliteCursor(DBPATH) as cur:
            cur.execute("INSERT INTO test_table(field) VALUES('one')")

    def add_two(self):
        with SqliteCursor(DBPATH) as cur:
            cur.execute("INSERT INTO test_table(field) VALUES('two')")

    def test_nest(self):
        with SqliteCursor(DBPATH) as cur:
            self.add_one()
            cur.execute(
                "INSERT INTO test_table(field) VALUES('one point five')")
            self.add_two()

        with SqliteCursor(DBPATH) as cur:
            cur.execute("SELECT COUNT(*) FROM test_table WHERE field='two'")
            row = cur.fetchone()
            self.assertEqual(row["COUNT(*)"], 1)


class AbortTest(unittest.TestCase):
    def setUp(self):
        schema(DBPATH)
        seed(DBPATH)
        SqliteCursor.DBPATH = DBPATH

    def tearDown(self):
        os.remove(DBPATH)

    def layer1(self):
        with SqliteCursor() as cur:
            cur.execute("INSERT INTO test_table(field) VALUES('X');")
            self.layer2()

    def layer2(self):
        with SqliteCursor() as cur:
            cur.execute("INSERT INTO test_table(field) VALUES('X');")
            raise HaltCommits

    def test_cascade_halt(self):
        with SqliteCursor() as cur:
            cur.execute("INSERT INTO test_table(field) VALUES('X');")
            self.layer1()

        with SqliteCursor() as cur:
            cur.execute("SELECT COUNT(*) FROM test_table WHERE field='X';")
            row = cur.fetchone()
            self.assertEqual(row['COUNT(*)'], 0)


db1 = os.path.join(FILEPATH, 'db1.db')
db2 = os.path.join(FILEPATH, 'db2.db')

class MultiDBTest(unittest.TestCase):


    def setUp(self):
        schema(db1)
        seed(db1)
        schema(db2)
        seed(db2)

    def tearDown(self):
        os.remove(db1)
        os.remove(db2)

    def success1(self):
        with SqliteCursor(db1) as cur:
            cur.execute("INSERT INTO test_table(field) VALUES('S1');")
            self.success2()

    def success2(self):
        with SqliteCursor(db2) as cur:
            cur.execute("INSERT INTO test_table(field) VALUES('S2');")

    def fail1(self):
        with SqliteCursor(db1) as cur:
            cur.execute("INSERT INTO test_table(field) VALUES('F1');")
            self.fail2()

    def fail2(self):
        with SqliteCursor(db2) as cur:
            cur.execute("INSERT INTO test_table(field) VALUES('F2');")
            raise HaltCommits

    def test_success(self):
        self.success1()
        with SqliteCursor(db1) as cur:
            cur.execute("SELECT COUNT(*) FROM test_table WHERE field='S1';")
            self.assertEqual(cur.fetchone()['COUNT(*)'], 1)

        with SqliteCursor(db2) as cur:
            cur.execute("SELECT COUNT(*) FROM test_table WHERE field='S2';")
            self.assertEqual(cur.fetchone()['COUNT(*)'], 1)

    def test_failure(self):
        self.fail1()
        with SqliteCursor(db1) as cur:
            cur.execute("SELECT COUNT(*) FROM test_table WHERE field='F1';")
            self.assertEqual(cur.fetchone()['COUNT(*)'], 0)

        with SqliteCursor(db2) as cur:
            cur.execute("SELECT COUNT(*) FROM test_table WHERE field='F2';")
            self.assertEqual(cur.fetchone()['COUNT(*)'], 0)
