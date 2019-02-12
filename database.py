import sqlite3

path_database = "base.db"

connect = sqlite3.connect(path_database)
cursor = connect.cursor()

view_data = (
    'Number',
    'Name',
    'Link',
    'Price',
    'Profile',
    'Information',
    'Address')

view_data_telegram = (
    'Id_external',
    'Number',
    'Name',
    'Seen',
    'Profile')


# Common
def _exe_raw_sql(sql):
    try:
        cursor.execute(sql)
        fetchall = cursor.fetchall()
    except sqlite3.DatabaseError as err:
        raise err
    else:
        connect.commit()
    return fetchall


# People
def create_bd():
    sql = """
    CREATE TABLE if not exists people(
        Id INTEGER PRIMARY KEY UNIQUE,
        Number VARCHAR(255) NOT NULL,
        Name VARCHAR(255) NOT NULL,
        Link VARCHAR(255),
        Price VARCHAR(255),
        Profile VARCHAR(255),
        Information VARCHAR(255),
        Address VARCHAR(255),
        CONSTRAINT unique_local UNIQUE (Number)
        );
    """
    _exe_raw_sql(sql)


def insert_into_table(
        number, name, link=None, price=None,
        profile=None, information=None, address=None):
    data = dict(zip(view_data,
                    [number, name, link, price, profile, information, address]))

    cols = ', '.join("'{}'".format(col) for col in data.keys())
    vals = ', '.join(':{}'.format(col) for col in data.keys())
    sql = 'INSERT INTO people ({}) VALUES ({})'.format(cols, vals)
    try:
        cursor.execute(sql, data)
    except sqlite3.DatabaseError as err:
        raise err
    connect.commit()


def get_all():
    sql = "SELECT * FROM people;"
    return _exe_raw_sql(sql)


#  Filters People
def filter_by_links(links):
    """links should be set, Return Set of links for processing"""

    assert isinstance(links, set)

    sql = "SELECT Link FROM people WHERE Link in ({});".format(
        ', '.join(["'{}'".format(item) for item in links]))
    resp = _exe_raw_sql(sql)
    return set(links) - set([item[0] for item in resp])


def is_not_phone_exists(phone):
    """Return True or False"""

    sql = "SELECT Number FROM people WHERE Number is '{}';".format(phone)
    resp = _exe_raw_sql(sql)
    return not any(resp)


# Telegram
def create_bd_telegram():
    sql = """
    CREATE TABLE if not exists telegram(
        Id_external INTEGER,
        Number VARCHAR(20) NOT NULL,
        Name VARCHAR(100) NOT NULL,
        Seen VARCHAR(30),
        Profile VARCHAR(255),
        CONSTRAINT unique_local UNIQUE (Number)
        );
    """
    _exe_raw_sql(sql)


# ToDo Drop hardcode
def insert_into_telegram(number, name, _id=1, seen=None, profile=None):
    data = dict(zip(view_data_telegram, (_id, number, name, seen, profile)))

    cols = ', '.join("'{}'".format(col) for col in data.keys())
    vals = ', '.join(':{}'.format(col) for col in data.keys())
    sql = 'INSERT INTO telegram ({}) VALUES ({})'.format(cols, vals)
    try:
        cursor.execute(sql, data)
    except sqlite3.DatabaseError as err:
        raise err
    connect.commit()


# ToDo change verification of Phone to verification of ID (id_external)
def is_telegram_acount(phone):
    """Return True or False"""

    sql = "SELECT Number FROM telegram WHERE Number is '{}';".format(phone)
    resp = _exe_raw_sql(sql)
    return any(resp)


def get_all_from_telegram():
    sql = "SELECT * FROM telegram;"
    return _exe_raw_sql(sql)


def get_user_from_telegram(phone):
    sql = "SELECT * FROM telegram WHERE Number is '{}';".format(phone)
    return _exe_raw_sql(sql)
