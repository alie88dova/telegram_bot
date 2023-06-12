import sqlite3
from database.db_tools import sql_connection


async def getFullBlockFromBlockId(block_id: int,state: int, conn: sqlite3.Connection):
    try:
        cur = conn.cursor()

        block = cur.execute(
            f"SELECT * FROM ZeroNovelBlocks WHERE BlockId={block_id} and StateUserChose={state}"
        )
        block = block.fetchall()
        print(block)
        return  {
            "id":block[0][0],
            "stateUserChose":block[0][1],
            "blockId":block[0][2],
            "blockText":block[0][3],
            "blockImageType":block[0][4],
            "blockImageIdificatore":block[0][5],
            "modify":block[0][6],
            "button_text":block[0][7],
        }
    except Exception as e:
        print(e)


async def getNovelbyId(novel_id:int, conn)->dict:
    """Возвращает всю сторку c данным id"""
    try:

        cur = conn.cursor()

        novel = cur.execute(
            f"SELECT * FROM Novels where id = {novel_id}"
        )
        novel = novel.fetchall()[0]
        return {
            "id": novel[0],
            "NovelName": novel[1],
            "NovelContnentType": novel[2],
            "NovelContentIdificatore": novel[3],
            "call_data": novel[4]
        }
    except Exception as e:
        print(e)


async def getUserChoises(tg_id:int, conn:sqlite3.Connection)->int:
    cur = conn.cursor()
    result = cur.execute(
        f"SELECT state_choose_1,state_choose_2,state_choose_3,state_choose_4,state_choose_5 FROM UserChooseNovelZero where tg_id = {tg_id}"
    )
    return result.fetchall()[0]


async def ComeUserToNovelZero(tg_id:int, conn:sqlite3.Connection):
    """Регестрирует первый вход пользователя в эту новвелу"""
    try:
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO UserChooseNovelZero (tg_id) values ({tg_id})"
        )
        print(1)
        cur.execute(
            f"Update UserChooseNovelZero set state_choose_1=1, id_block_now=1 where tg_id = {tg_id}"
        )
        print(1)
        conn.commit()
    except Exception as e:
        print(e)


async def get_user_state(tg_id,conn) -> int:
    """Возвращает число номер главного не за нуленного"""
    states = await getUserChoises(tg_id,conn)
    print(states)

    if states[4] == 1:
        return 4
    if states[3] == 1:
        return 3
    if states[2] == 1:
        return 2
    if states[1] == 1:
        return 1
    if states[0] == 1:
        return 0


async def get_user_in_novel_position(tg_id, conn):
    cur = conn.cursor()
    d = cur.execute(
        f"SELECT id_block_now FROM UserChooseNovelZero where tg_id ={tg_id}"
    )
    d=d.fetchall()[0][0]
    return d


async def update_user_id_block(tg_id, block_id,conn):
    cur = conn.cursor()
    cur.execute(
        f"update UserChooseNovelZero SET id_block_now={block_id} where tg_id = {tg_id}"
    )
    conn.commit()


async def get_content_to_dialog(block_id, dialog_indify,conn:sqlite3.Connection):
    cur = conn.cursor()
    dialog_content = cur.execute(
        f"SELECT DialogText , DialogContent FROM ZeroNovelDiologs WHERE BlockId={block_id} and DialogContentIdificatore={dialog_indify}"
    )
    dialog_content = dialog_content.fetchall()
    return dialog_content


async def update_choose_user(tg_id, choose_index, con:sqlite3.Connection):
    cur = con.cursor()
    cur.execute(
        f"update UserChooseNovelZero SET state_choose_{choose_index}=1 where tg_id = {tg_id}"
    )
    con.commit()


if __name__ == "__main__":
    conn = sql_connection()
    print(get_content_to_dialog(2,0,conn))