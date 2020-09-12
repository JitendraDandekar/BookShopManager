import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS bookmanager(id integer primary key autoincrement, bookname text, publication text, author text, price int, availability text, quantity text, comment text)")
        self.conn.commit()

    def insert(self, entities):
        self.cur.execute("INSERT INTO bookmanager(bookname, publication, author, price, availability, quantity, comment) VALUES(?,?,?,?,?,?,?)", entities)
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT bookname, publication, author, price, availability, quantity, comment FROM bookmanager order by bookname")
        data = self.cur.fetchall()
        return data

    def delete(self, no):
        self.cur.execute("DELETE FROM bookmanager WHERE id=?", (no,))
        self.conn.commit()
    
    def match(self):
        self.cur.execute("SELECT * FROM bookmanager ORDER BY bookname")
        rows = self.cur.fetchall()
        return rows

    def update(self, bookname, publication, author, price, availability, quantity, comment, no):
        self.cur.execute("UPDATE bookmanager SET bookname=?, publication=?, author=?, price=?, availability=?, quantity=?, comment=? WHERE id=?", (bookname, publication, author, price, availability, quantity, comment, no))
        self.conn.commit()

    def search(self, bookname, publication, author):
        self.cur.execute("SELECT bookname, publication, author, price, availability, quantity, comment FROM bookmanager WHERE lower(bookname) like ? OR lower(publication) like ? OR lower(author) like ? order by bookname",(bookname, publication, author))
        data = self.cur.fetchall()
        return data

    def __del__(self):
        self.conn.close()
