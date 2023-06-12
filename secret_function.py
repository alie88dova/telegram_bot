

async def index_counter_fix(index, max_value) -> int:
    """Возвращает index"""

    if index >= max_value-1:
        index = max_value-1
    elif index < 0:
        index = 0

    return index

def test_secret_func():
    print("Секрет активирован")