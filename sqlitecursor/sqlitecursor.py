from sqlitecursor.singleton import Singleton
import sqlite3


class HaltCommits(Exception):
    pass


class SqliteCursor(Singleton):
    """ SqliteCursor(dbpath=None, rowkeys=True, *args, **kwargs) Context
returning a sqlite3 cursor. dbpath defaults to SqliteCursor.DBPATH, rowkeys
gives fetch results named indicies, additional args are passed to
sqlite3.connect. SqliteCursor uses the Singleton pattern. Setting
SqliteCursor.DBPATH sets a global default."""

    DBPATH = '_sqlitecursor.db'
    connections = {}
    pathstack = []

    def __init__(self, dbpath=None, rowkeys=True, *args, **kwargs):
        path = self.DBPATH
        if dbpath is not None:
            path = dbpath
        elif len(self.pathstack) > 0:
            path = self.pathstack[-1]
        self.pathstack.append(path)

        if path not in self.connections.keys():
            # if path has not yet been seen, open a connection for it
            self.connections[path] = sqlite3.connect(path, *args, **kwargs)

            if rowkeys:
                # fetch results have named indexing
                self.connections[path].row_factory = sqlite3.Row

    def __enter__(self):
        return self.connections[self.pathstack[-1]].cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.pathstack.pop()

        if not exc_type and len(self.pathstack) == 0:
            # stack clear & no exceptions => commit & close all
            while self.connections:
                _, connection = self.connections.popitem()
                connection.commit()
                connection.close()

        elif len(self.pathstack) == 0:
            # stack clear & exception => rollback and close all
            while self.connections:
                _, connection = self.connections.popitem()
                connection.rollback()
                connection.close()

            if exc_type == HaltCommits:
                # stack clear & HaltCommit exception => catch the HaltCommit
                return True

        # stack not clear => leave connections open & uncommitted & propagate
        # exceptions
