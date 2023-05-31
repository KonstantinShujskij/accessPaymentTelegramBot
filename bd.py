import sqlite3
from utils import Struct

db_name = "partners.db"


def insert(db, telegram_id, api_id='undefined', status='check'):
    query = """ INSERT INTO partners (telegram, api, status) VALUES (?, ?, ?)"""
    data = (telegram_id, api_id, status)

    try:
        cursor = db.cursor()
        cursor.execute(query, data)

        db.commit()
    except sqlite3.IntegrityError:
        pass


def init():
    database = sqlite3.connect(db_name)
    data = database.cursor()

    data.execute("CREATE TABLE IF NOT EXISTS partners("
                 "id integer primary key,"
                 "telegram TEXT NOT NULL,"
                 "api TEXT NOT NULL,"
                 "status TEXT NOT NULL"
                 ");")

    database.commit()
    database.close()


def create_new_partner(telegram_id):
    db = sqlite3.connect(db_name)
    insert(db, telegram_id)


def ban_partner(telegram_id):
    db = sqlite3.connect(db_name)

    cursor = db.cursor()
    cursor.execute("""UPDATE partners SET status = ? WHERE telegram = ?""", ('ban', telegram_id))

    db.commit()
    db.close()


def reban_partner(telegram_id):
    db = sqlite3.connect(db_name)

    cursor = db.cursor()
    cursor.execute("""UPDATE partners SET status = ? WHERE telegram = ?""", ('allow', telegram_id))

    db.commit()
    db.close()


def wait_partner(telegram_id):
    db = sqlite3.connect(db_name)

    cursor = db.cursor()
    cursor.execute("""UPDATE partners SET status = ? WHERE telegram = ?""", ('check', telegram_id))

    db.commit()
    db.close()


def refresh_partner(telegram_id):
    db = sqlite3.connect(db_name)

    cursor = db.cursor()
    cursor.execute("""UPDATE partners SET status = ? WHERE telegram = ?""", ('allow', telegram_id))

    db.commit()
    db.close()


def allow_partner(telegram_id, access_id):
    db = sqlite3.connect(db_name)

    cursor = db.cursor()
    cursor.execute("""UPDATE partners SET status = ?, api = ? WHERE telegram = ?""", ('allow', access_id, telegram_id))

    db.commit()
    db.close()


def clear_partner(telegram_id):
    db = sqlite3.connect(db_name)

    cursor = db.cursor()
    cursor.execute("""DELETE from partners WHERE telegram = ?""", (str(telegram_id),))

    db.commit()
    db.close()


def get_partner(telegram_id):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM partners WHERE telegram = ?""", (str(telegram_id),))
    data = cursor.fetchone()
    db.close()

    if not data:
        return None

    (_id, telegram, api_id, status) = data

    return Struct(**{
        'telegram_id': telegram,
        'api_id': api_id,
        'status': status
    })

