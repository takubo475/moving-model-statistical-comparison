import builtins
import sqlite3

class Sql_controller():
    def __init__(self,name=None):
        if name:
            dbname=str(name)
        else:
            dbname = 'main.db'

        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()

        # テーブルの作成
        self.cur.execute(
            'CREATE TABLE if not exists expart(id INTEGER PRIMARY KEY AUTOINCREMENT, startpos STRING,goalpos STRING, reward INTEGER ,step INTEGER , route STRING)'
        )
        self.bulktable=list()

    def insert(self,values):#遅いので複数ある場合はバルクインサート
        self.bulktable.append(values)
        if len(self.bulktable)>=10000:
            self.bulkinsert()
            self.bulktable=list()

    
    def bulkinsert(self):
        self.cur.executemany('INSERT INTO expart ( startpos, goalpos, reward ,step ,route ) values(?, ?, ?, ?, ? )',self.bulktable)

        self.conn.commit()