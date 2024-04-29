import pymysql.cursors

conn = pymysql.connect(host='myfirstproject.c94g44mqus56.ap-northeast-1.rds.amazonaws.com',
                    user='admin',
                    password = 'D5H3bomrfLKtRW7geo31',
                    db='tip_line_schema',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)
def select_users(conn):
    with conn.cursor() as cur:
        try:
            cur.execute("select * from User;")

            for row in list(cur):
                # Try getting profile
                print(row)
            conn.commit()
        except Exception as e:
            raise ValueError(str(e))
def history_tip(conn, user_id):
    result = []
    with conn.cursor() as cur:
        try:
            cur.execute(f"select date, amount_bill, percentage, (amount_bill * percentage) as Total from TipHistory where tip_user_id = '{user_id}' order by date desc;")

            #for row in list(cur):
                # Try getting profile
            return list(cur)

            #conn.commit() when its for insert and delete
        except Exception as e:
            raise ValueError(str(e))
#{'date': datetime.date(2024, 4, 29), 'amount_bill': 40, 'percentage': 10, 'Total': 400}
def convertTomessage(data):

    return f'[{data["date"].year}/{data["date"].month}/{data["date"].day}] ${data["amount_bill"]} + {data["percentage"]}% → Total ${data["Total"]}'

def convertAllmessage(tips):
    result = ""
    for tip in tips:
        result = result + convertTomessage(tip) + "\n"

    return result

if __name__ == "__main__":
    select_users(conn)
    tips = history_tip(conn, 'A1')
    print(tips)

    #print(convertTomessage(tips[1]))
    print(convertAllmessage(tips))
