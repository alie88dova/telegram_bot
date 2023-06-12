from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import datetime
import sqlite3


def sql_connection() -> sqlite3.Connection:
    """Create connection to db"""
    try:
        con = sqlite3.connect('F:/bots/bot_obidinostV3/obidinost.db')

        return con
    except sqlite3.Error as e:
        print(f"{e}")


async def register(con: sqlite3.Connection, user):
    """Add new user to table users"""

    cur = con.cursor()

    users = cur.execute(
        f"SELECT tg_id FROM Users "
    )

    a=users.fetchall()
    print(a, "!!!!!!!!")
    for i in a:
        print(f"i= {i}")
        print(f"msg_tg={user}")
        if int(user) == int(i[0]):
            return "reg"
    cur.execute(
        f"INSERT INTO Users(tg_id, permission, position) VALUES ({user}, 'user', 'banner') ;"
    )

    con.commit()


async def position_now(con: sqlite3.Connection, chat_id: int, id_message: int):
    cur = con.cursor()
    cur.execute(
        f"UPDATE Users SET position={id_message} where tg_id={chat_id}"
    )
    con.commit()
    print(f"user={chat_id} | id_message={id_message}")


async def get_user_last_msg(tg, con):
    cur = con.cursor()
    user = cur.execute(
        f"SELECT position FROM Users where tg_id={tg}"
    )

    return user.fetchall()[0][0]


async def check_sub(tg_id:int ,conn: sqlite3.Connection):
    cur = conn.cursor()

    a = cur.execute(
        f"SELECT type_sub FROM Users WHERE tg_id='{tg_id}'"
    )

    return a.fetchall()[0][0] #TYPE SUB



async def give_novels(con: sqlite3.Connection, id_novel:int=1) -> dict:
    """Return dict"""
    cur = con.cursor()

    content = cur.execute(
        f"SELECT * FROM Novels WHERE id='{id_novel}';"
    )
    content = content.fetchall()

    if not content:
        return {}

    content = content[0]
    c = {
        "id": content[0],
        "desc": content[1],
        "content_id": content[2],
        "file_path": content[3],
        "content_type": content[4],
        "secret_id": content[5]
    }

    return c


async def give_chapter(con: sqlite3.Connection, id_novel:int, id_chapter:int=1):
    """Return chapter"""
    cur = con.cursor()

    chapters = cur.execute(
        f"SELECT * FROM Chapters WHERE id_novel='{id_novel}'; "
    )
    chapters = chapters.fetchall()
    rowcount = len(chapters)

    if not chapters:
        return {"chapter_count": rowcount}

    if rowcount <= id_chapter-1:
        return {"chapter_count": rowcount}

    content = chapters[id_chapter-1]

    c = {
        "id": content[0],
        "id_novel": content[1],
        "desc": content[2],
        "content_id": content[3],
        "file_path": content[4],
        "content_type": content[5],
        "secret_id": content[6],
        "chapter_count": rowcount,
    }

    return c


async def give_block(con: sqlite3.Connection, id_novel:int, id_chapter:int, id_block:int=0):
    """Return chapter"""
    cur = con.cursor()

    blocks = cur.execute(
        f"SELECT * FROM Blocks WHERE id_chapter ='{id_chapter}'"
    )
    blocks = blocks.fetchall()
    rowcount = len(blocks)
    print(blocks)
    if not blocks:
        return {}
    print(rowcount)
    if rowcount <= id_block - 1:
        return {"blocks_count": rowcount}

    content = blocks[id_block - 1]

    c = {
        "id": content[0],
        "id_novel": content[1],
        "desc": content[2],
        "content_id": content[3],
        "file_path": content[4],
        "content_type": content[5],
        "secret_id": content[6],
        "blocks_count": rowcount,
    }

    return c


async def get_user(conn:sqlite3.Connection) -> list:
    cur = conn.cursor()

    users = cur.execute(
        f"SELECT * FROM Users;"
    )
    users = users.fetchall()
    return users


async def get_sub_type(conn: sqlite3.Connection, tg_id:int) -> str:
    cur = conn.cursor()

    sub = cur.execute(
        f"SELECT type_sub FROM Users where tg_id = {tg_id};"
    )
    sub = sub.fetchall()
    return sub

async def novel_count(conn: sqlite3.Connection) -> int:

    cur = conn.cursor()
    novels = cur.execute(
        f"SELECt * from Novels"
    )
    return len(novels.fetchall())


async def check_priv(conn: sqlite3.Connection, tg_id) -> str:

    cur = conn.cursor()
    priv = cur.execute(
        f"SELECt permission from Users where tg_id={tg_id}"
    )
    priv = priv.fetchall()
    priv = priv[0][0]
    return priv


#фунция для провеки кода
async def check_cor_activate(user_tg_id: int, code:str, conn: sqlite3.Connection):
    """

    :param user_tg_id:
    :param code:
    :param conn:
    :return 0 если не подписка не верна, 1 покупка подписки:
    """

    cur = conn.cursor()
    free_codes = cur.execute(
        f"SELECT * FROM ActivateCodes WHERE tg_id = 0 and act_code = '{code}'"
    )
    free_codes = free_codes.fetchall()
    if free_codes == []:
        return 0

    cur.execute(
        f"UPDATE ActivateCodes set tg_id = '{user_tg_id}' WHERE tg_id = 0 and act_code = '{code}'"
    )
    #В будующем заменится на провеку типа подписки
    cur.execute(
        f"UPDATE Users set type_sub = 'Предзаказ' WHERE tg_id = '{user_tg_id}'"
    )
    conn.commit()
    return 1


async def update_type_sub(conn: sqlite3.Connection,user_tg_id: int):
    """
        Обновляет тип подписки пользователя после корректной оплаты
    """
    cur = conn.cursor()
    cur.execute(
        f"UPDATE Users set type_sub = 'Предзаказ' WHERE tg_id = '{user_tg_id}'"
    )
    conn.commit()


async def check_type_sub(conn: sqlite3.Connection, user_tg_id):
    """
    Возвращает тип подписки пользователя с данным id
    если пользователя не найдено возврщает 0
    :return:str Тип подписки
    """
    try:
        cur = conn.cursor()
        type_sub = cur.execute(
            f"SELECT type_sub FROM Users WHERE tg_id = '{user_tg_id}'"
        )
        type_sub = type_sub.fetchall()
        type_sub = type_sub[0][0]
        return type_sub
    except Exception as e:
        return 0




if __name__ == "__main__":
    print("Зачем ты тут")
    conn = sql_connection()
    print(check_type_sub(conn, 6791070701))