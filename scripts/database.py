import sqlite3


class Database:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS credentials
                         (id INTEGER PRIMARY KEY, date TEXT DEFAULT(CURRENT_DATE), title TEXT, login TEXT, password TEXT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS masterPassword
                         (id INTEGER PRIMARY KEY, date TEXT DEFAULT(CURRENT_DATE), masterPassword TEXT)''')
        self.conn.commit()

    def insertMasterPwd(self, masterPassword):
        self.cur.execute(
            '''INSERT INTO masterPassword(masterPassword) VALUES (?)''', (masterPassword,))
        self.conn.commit()

    def updateMasterPwd(self, new_hash):
        self.cur.execute(
            '''UPDATE masterPassword SET masterPassword=? WHERE id=1''', (new_hash,))
        self.conn.commit()

    def readMasterPwd(self):
        self.cur.execute('''SELECT masterPassword FROM masterPassword''')
        self.conn.commit()

        return self.cur.fetchone()

    def insertCred(self, title, login, password):
        self.cur.execute('''INSERT INTO credentials(title, login, password) VALUES
                            (? , ?, ?)''', (title, login, password))
        self.conn.commit()

    def readCred(self, id=None, title=None, login=None):
        if id == None and title == None and login == None:
            self.cur.execute("SELECT * FROM credentials")
        elif login == None and id == None:
            self.cur.execute('''SELECT * FROM credentials
                                WHERE title = ?''', (title,))
        elif id == None and title == None:
            self.cur.execute('''SELECT * FROM credentials
                                WHERE login = ?''', (login,))
        elif id != None:
            self.cur.execute('''SELECT * FROM credentials
                                WHERE id = ?''', (id,))
        self.conn.commit()

        return self.cur.fetchall()

    def delCred(self, id):
        self.cur.execute('''DELETE FROM credentials
                            WHERE id = ?''', str(id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
