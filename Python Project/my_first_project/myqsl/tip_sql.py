import pymysql.cursors
import json
import uuid
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
            cur.execute(f"select date, amount_bill, percentage, (amount_bill * percentage/ 100 + amount_bill) as Total from TipHistory where tip_user_id = '{user_id}' order by date desc;")

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

def jason_insert(amount_bill):
    return {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": f"Leave Tip for Bill {amount_bill} ?",
                "weight": "bold",
                "color": "#555555",
                "align": "center",
                "size": "xl"
              },
              {
                "type": "separator"
              }
            ],
            "spacing": "lg"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "size": "xl",
                "color": "#555555",
                "action": {
                  "type": "postback",
                  "label": "you current bill",
                  "data": "hello"
                },
                "text": "Please enter a tip"
              }
            ],
            "spacing": "md"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "align": "center",
                "size": "lg",
                "weight": "bold",
                "text": "10%"
              }
            ],
            "backgroundColor": "#D3D3D3",
            "cornerRadius": "xxl",
            "width": "240px",
            "height": "44px",
            "paddingTop": "md",
            "action": {
              "type": "postback",
              "label": "percentage",
              "data": f"Bill 10% {amount_bill}",
              "displayText": "Tipped 10%"
            }
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "15%",
                "align": "center",
                "size": "lg",
                "weight": "bold"
              }
            ],
            "backgroundColor": "#D3D3D3",
            "cornerRadius": "xxl",
            "width": "240px",
            "height": "44px",
            "paddingTop": "md",
            "action": {
              "type": "postback",
              "label": "percentage",
              "data": f"Bill 15% {amount_bill}",
              "displayText": "Tipped 15%"
            }
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "20%",
                "align": "center",
                "size": "lg",
                "weight": "bold"
              }
            ],
            "paddingTop": "md",
            "width": "240px",
            "height": "44px",
            "backgroundColor": "#D3D3D3",
            "cornerRadius": "xxl",
            "action": {
              "type": "postback",
              "label": "percentage",
              "data": f"Bill 15% {amount_bill}",
              "displayText": "Tipped 20%"
            }
          }
        ],
        "spacing": "xl"
      },
      "footer": {
        "type": "box",
        "layout": "vertical",
        "contents": [],
        "justifyContent": "center",
        "alignItems": "center",
        "paddingTop": "4px"
      }
    }

def amount_bill_process_postback(postback_data, tip_user_id:str):
    if postback_data[:5] == 'Bill ':
        percent_bill_amount = postback_data.replace("Bill ", "")
        # ->"10% 200"
        # [abnormal] Bill 10 200
        percent_bill_amount_list = percent_bill_amount.split("% ")
        # ->["10","200"]

        # error check
        if len(percent_bill_amount_list) == 2 and percent_bill_amount_list[0].isdigit() and percent_bill_amount_list[1].isdigit():
            insert_amount_bill(int(percent_bill_amount_list[0]), int(percent_bill_amount_list[1]), tip_user_id)
            return True
        else:
            return False
    else:
        False
def check_user(user_id):
    ## Check if user_id is in User table
    user_data_list = []
    with conn.cursor() as cur:
        try:
            cur.execute(f"select user_id from User;")

            user_data_list = list(cur)


        except Exception as e:
            raise ValueError(str(e))

    #user_list = [{"user_id": "A1", "name": "John"}, {"user_id": "A2", "name": "John"}, {"user_id": "A3", "name": "John"}]

    user_list = []
    for user_data in user_data_list:
        user_list.append(user_data["user_id"])


    if user_id not in user_list:

        with conn.cursor() as cur:
            try:
                sql = f"insert into User values ('{user_id}', '');"
                print("[Inserting... -> ]" + sql)
                cur.execute(sql)

                conn.commit()
            except Exception as e:
                raise ValueError(str(e))
        return
def insert_amount_bill(percentage:int, amount_bill:int,tip_user_id:str):
    check_user(tip_user_id)
    with conn.cursor() as cur:
        try:
            random_history_uuid = uuid.uuid4()
            sql = f"insert into TipHistory Values ('{random_history_uuid}', {amount_bill}, {percentage}, curdate(), '{tip_user_id}');"
            print(sql)
            cur.execute(sql)

            # for row in list(cur):
            # Try getting profile

            conn.commit()
        except Exception as e:
            raise ValueError(str(e))



if __name__ == "__main__":
    select_users(conn)
    tips = history_tip(conn, 'A1')
    print(tips)

    #print(convertTomessage(tips[1]))
    print(convertAllmessage(tips))

    with open("output.json", "w") as f:
        json.dump(jason_insert(200), f)
    #test = amount_bill_get(conn, 40, 'A7')
    #print(test)
    #amount_bill_process_postback("Bill 25% 800")
    tips = history_tip(conn, 'A1')
    print(convertAllmessage(tips))


    insert_amount_bill(10, 250, 'c1')

