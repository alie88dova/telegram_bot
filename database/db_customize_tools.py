import sqlite3

from database.db_tools import sql_connection


async def get_menu_name(tg_id: int, conn: sqlite3.Connection) -> str:
    """

    :param tg_id:
    :param conn:
    :return STRING with name user to use in menu:
    """
    cur = conn.cursor()
    name = cur.execute(
        f"SELECT menu_name FROM Users where tg_id = {tg_id}"
    )

    name = name.fetchall()
    name = name[0][0]



    return name


async def get_menu_screen(tg_id: int, conn: sqlite3.Connection):
    """

    :param tg_id:
    :param conn:
    :return STRING with name user to use in menu:
    """
    cur = conn.cursor()
    name = cur.execute(
        f"SELECT Screen FROM Users where tg_id = {tg_id}"
    )
    print(1)

    name = name.fetchall()

    name = name[0][0]
    try:
        d = cur.execute(
            f"SELECT screen FROM Screens where id = {name}"
        )
        d = d.fetchall()
        d = d[0][0]
    except Exception as e:
        return 0
    return d



async def update_menu_name(tg_id, new_name, conn:sqlite3.Connection):
    """

    :param tg_id:
    :param new_name:
    :param conn:
    :return NONE:
    """
    cur = conn.cursor()
    cur.execute(
        f"UPDATE Users set menu_name = '{new_name}' where tg_id = {tg_id}"
    )
    conn.commit()


async def update_screen(tg_id, screen_id, conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute(
        f"UPDATE Users SET Screen = {screen_id} WHERE tg_id = {tg_id}"
    )
    conn.commit()


async def get_screen(id_now: int, conn: sqlite3.Connection):
    """
    Возвращает экран по id
    :param id_now:
    :param conn:
    :return: Строку с file_id данного фона
    """
    cur = conn.cursor()
    screen = cur.execute(
        f"SELECT screen FROM Screens where id = {id_now}"
    )
    screen = screen.fetchall()
    screen = screen[0][0]
    return screen


async def get_quanity_screens(conn: sqlite3.Connection) -> int:
    """
    :param conn:
    :return int quanity of screens in database now:
    """

    cur = conn.cursor()
    quan = cur.execute(
        f"SELECT * FROM Screens"
    )
    quan = quan.fetchall()

    return len(quan)


if __name__ == "__main__":
    a = 5
    d = {}
    d.sorted()
    b =1
    print('a', a + 3)
    print(a)