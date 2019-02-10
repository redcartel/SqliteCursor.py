# SqliteCursor 0.1

## a more robust context for python sqlite3 connections

author: Carter Adams

context maintains a pool of connections (only one per db) that do not commit or close until the outermost `with as` block resolves with no exceptions.

sqlitecursor.HaltCommits can be raised to rollback all connections.

```python
with SqliteCursor('mydata.db') as cur:
    cur.execute("INSERT INTO tab(field) VALUES(?);", ('one',))
    with SqliteCursor('anotherdb.db') as cur2:
        cur2.execute("INSERT INTO something(name1, name2) VALUES(?, ?);", ('a', 'b'))
        raise HaltCommits

# no changes will be written to either db
```

This works across function calls and modules.

SqliteCursor is a singleton class and setting SqliteCursor.DBPATH sets a global default database

If a SqliteCursor() context is entered with a default argument inside of another SqliteCursor() context, it returns the parent context's connection rather than the global default.

copyleft. Use & abuse it, whatever.
