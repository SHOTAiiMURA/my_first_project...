import pymysql.cursors

conn = pymysql.connect(host='myfirstproject.c94g44mqus56.ap-northeast-1.rds.amazonaws.com',
                    user='admin',
                    password = 'D5H3bomrfLKtRW7geo31',
                    db='my_db',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)

def my_db(conn):
    with conn.cursor() as cur:
        try:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS my_db.Priority (
  priority VARCHAR(10) NOT NULL,
  PRIMARY KEY (priority),
  UNIQUE INDEX priority_UNIQUE (priority ASC) VISIBLE)
ENGINE = InnoDB;
                """
            )
            cur.execute(
                """
    CREATE TABLE IF NOT EXISTS my_db.User (
      line_id VARCHAR(45) NOT NULL,
      name VARCHAR(45) NULL,
      PRIMARY KEY (line_id))
    ENGINE = InnoDB;
                """
            )

            cur.execute(
                """
    CREATE TABLE IF NOT EXISTS my_db.Task (
      task_id INT NOT NULL AUTO_INCREMENT,
      name VARCHAR(100) NULL,
      duration INT NULL,
      state CHAR(2) NOT NULL,
      due_date DATETIME NULL,
      end_time DATETIME NULL,
      start_time DATETIME NULL,
      extended_time INT NOT NULL DEFAULT 0,
      priority VARCHAR(10) NULL,
      line_id VARCHAR(45) NOT NULL,
      PRIMARY KEY (task_id),
      UNIQUE INDEX task_id_UNIQUE (task_id ASC) VISIBLE,
      INDEX fk_Task_Priority1_idx (priority ASC) VISIBLE,
      INDEX fk_Task_User1_idx (line_id ASC) VISIBLE,
      CONSTRAINT fk_Task_Priority1
        FOREIGN KEY (priority)
        REFERENCES my_db.Priority (priority)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
      CONSTRAINT fk_Task_User1
        FOREIGN KEY (line_id)
        REFERENCES my_db.User (line_id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION)
    ENGINE = InnoDB;
                """
            )
            conn.commit()
        except Exception as e:
            print("Error")
            raise ValueError(str(e))

def show_tables(conn):
    with conn.cursor() as cur:
        try:
            cur.execute("show tables;")

            for row in list(cur):
                # Try getting profile
                print(row)
            conn.commit()
        except Exception as e:
            raise ValueError(str(e))

def insert_priorities(conn,priority):
    with conn.cursor() as cur:
        try:
            cur.execute(f"Insert ignore into Priority (priority) Values('{priority}');")
            conn.commit()
        except Exception as e:
                raise ValueError(str(e))

def select_priorities(conn):
    with conn.cursor() as cur:
        try:
            cur.execute("select * from Priority;")

            for row in list(cur):
                # Try getting profile
                print(row)
            conn.commit()
        except Exception as e:
            raise ValueError(str(e))


def drop_table(conn):
    with conn.cursor() as cur:
        try:
            cur.execute("SET foreign_key_checks = 0;")
            #cur.execute("Drop Table Priority")
            #cur.execute("Drop Table Task")
            #cur.execute("Drop Table User")
            conn.commit()
        except Exception as e:
            raise ValueError(str(e))


select_priorities(conn)
insert_priorities(conn,"high")
insert_priorities(conn,"medium")
insert_priorities(conn,"low")