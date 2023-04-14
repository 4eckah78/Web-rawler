import pytest
import time
from datetime import datetime
import os.path
from web_crawler.main import get_posts_by_q
from web_crawler.main import get_data

# Проверка на существование файла для СПБГУ
def test_1():
    q = "#СПбГУ"
    date_time = datetime(2023, 3, 13, 0, 0)
    start_time = int(time.mktime(date_time.timetuple()))
    get_posts_by_q(q, start_time=start_time)
    assert os.path.exists("posts_SPbU.csv") == True

# # Проверка на существование файла для МГУ
def test_2():
    q = "#МГУ"
    date_time = datetime(2023, 3, 13, 0, 0)
    start_time = int(time.mktime(date_time.timetuple()))
    get_posts_by_q(q, start_time=start_time)
    assert os.path.exists("posts_MGU.csv") == True

# # Проверка на подачу обычного текста на русском
def test_3():
    q = "Просто текст"
    date_time = datetime(2023, 3, 13, 0, 0)
    start_time = int(time.mktime(date_time.timetuple()))
    with pytest.raises(ValueError):
        get_posts_by_q(q, start_time=start_time)

# # Проверка на подачу обычного текста на английском
def test_4():
    q = "some text"
    date_time = datetime(2023, 3, 13, 0, 0)
    start_time = int(time.mktime(date_time.timetuple()))
    get_posts_by_q(q, start_time=start_time)

# # Проверка на подачу числа вместо текста
def test_5():
    q = 12345
    date_time = datetime(2023, 3, 13, 0, 0)
    start_time = int(time.mktime(date_time.timetuple()))
    with pytest.raises(ValueError):
        get_posts_by_q(q, start_time=start_time)

# # Проверка на подачу некорректной даты
def test_6():
    q = "#МГУ"
    date_time = datetime(2024, 3, 13, 0, 0)
    start_time = int(time.mktime(date_time.timetuple()))
    with pytest.raises(ValueError):
        get_posts_by_q(q, start_time=start_time)

# # Проверка на то что не подали q
def test_7():
    q = "#МГУ"
    date_time = datetime(2023, 3, 13, 0, 0)
    start_time = int(time.mktime(date_time.timetuple()))
    with pytest.raises(TypeError):
        get_posts_by_q(start_time=start_time)

def test_8():
    test_data = {"id": 123,
                 "from_id": 456,
                 "likes": {"count": 45},
                 "reposts": {"count": 52},
                 "text": "Some text",
                 "comments": {"count": 72},
                 "views": {"count": 100},
                 "date": "2023.03.14",
                 }
    assert get_data(test_data) == {
        "post_id": 123,
        "from_id": 456,
        "likes": 45,
        "reposts": 52,
        "text": "Some text",
        "comments": 72,
        "views": 100,
        "date": "2023.03.14",}

def test_9():
    test_data = {}
    assert get_data(test_data) == {
        "post_id": 0,
        "from_id": 0,
        "likes": "zero",
        "reposts": "zero",
        "text": "***",
        "comments": "zero",
        "views": "zero",
        "date": "zero",}

def test_10():
    q = "#СПбГУ"
    date_time = datetime(2023, 3, 13, 0, 0)
    start_time = int(time.mktime(date_time.timetuple()))
    get_posts_by_q(q, start_time=start_time)
    str_to_test = "Говард Лавкрафт «Хребты безумия»"
    with open('posts_SPbU.csv', 'rt', encoding="utf8") as c:
        str_arr_csv = c.readlines()
    assert str(str_to_test) in str(str_arr_csv)

def test_11():
    q = "#МГУ"
    date_time = datetime(2023, 3, 13, 0, 0)
    start_time = int(time.mktime(date_time.timetuple()))
    get_posts_by_q(q, start_time=start_time)
    str_to_test = "ЭКСКУРСИЯ В МУЗЕЙ ИСТОРИИ МГУ"
    with open('posts_MGU.csv', 'rt', encoding="utf8") as c:
        str_arr_csv = c.readlines()
    assert str(str_to_test) in str(str_arr_csv)

def test_12():
    q="#СПБГУ"
    end_time = datetime(2023, 4, 13, 0, 0)
    date_time = datetime(2023, 3, 13, 0, 0)
    end_time = int(time.mktime(end_time.timetuple()))
    start_time = int(time.mktime(date_time.timetuple()))
    assert get_posts_by_q(q, start_time=start_time, end_time=end_time) == 750

