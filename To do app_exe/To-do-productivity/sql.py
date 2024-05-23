import datetime

import pymysql.cursors

conn = pymysql.connect(host='tododbpy.c94g44mqus56.ap-northeast-1.rds.amazonaws.com',
                    user='admin',
                    password = '1qaz2wsx',
                    db='Tododb',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)


def check_connect(conn):
    with conn.cursor() as cur:
        try:
            cur.execute("select * from Task;")

            for row in list(cur):
                print(row)
        except Exception as e:
            raise ValueError(str(e))

## CRUD
### Create, Read, Update, Delete

## nt == new task
def create_task(conn, name, time, state, due_date:datetime.datetime, end_time:datetime.datetime, start_time:datetime.datetime, priority, line_id):
    with conn.cursor() as cur:
        try:
            cur.execute("insert into Task (name, duration, state, due_date, end_time, start_time, extended_time, priority, line_id) values ('{}', {}, '{}', cast('{}' as datetime ), cast('{}' as datetime ), cast('{}' as datetime ), 0, '{}', '{}');"
                        .format(name, time, state, due_date.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S'), start_time.strftime('%Y-%m-%d %H:%M:%S'), priority, line_id))

            conn.commit()
        except Exception as e:
            raise ValueError(str(e))
    return


def create_empty_task(task_name, due_date, priority, line_id):
    create_task(conn, task_name, 0, "nt", datetime.datetime(1970, 1, 1), datetime.datetime(1970, 1, 1), datetime.datetime(1970, 1, 1),
                "", line_id)


def create_low_task(task_name, duration, line_id):
    create_task(conn, task_name, duration, "nt", datetime.datetime(1970, 1, 1), datetime.datetime(1970, 1, 1),
                datetime.datetime(1970, 1, 1),
                "low", line_id)


def create_medium_task(task_name, duration, line_id):
    create_task(conn, task_name, duration, "nt", datetime.datetime(1970, 1, 1), datetime.datetime(1970, 1, 1),
                datetime.datetime(1970, 1, 1),
                "medium", line_id)


def create_high_task(task_name, duration, line_id):
    create_task(conn, task_name, duration, "nt", datetime.datetime(1970, 1, 1), datetime.datetime(1970, 1, 1),
                datetime.datetime(1970, 1, 1),
                "high", line_id)


## 1. task_name
## 2. duration
## 3. due_date
## 4. priority

#use for view task
def read_task(conn):
    return


## update product set price=340 where name='Grape';
def update_duration(conn):
    return

## Year, Month, Date, Hour, Minute
def update_due_date(conn):
    return

## datetime(year, 0, 0)
def update_year(conn):
    return

## datetime(5, 0, 0)
## 1. select
## 2. datetime(year, month, 0)
def update_month(conn):
    return

def update_priority(conn):
    return


def delete_task(conn):
    return


def create_user(conn):
    return


def read_user(conn):
    return


def delete_user(conn):
    return


if __name__ == "__main__":
    print("Hello World")
    # create_task(conn, "Taro", 3600, "nb", datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now(), "medium", "bbbbbb")
    create_empty_task("Laundry", 24,"High","ddddd")
    update_duration(1800)
    check_connect(conn)