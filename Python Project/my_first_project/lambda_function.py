import os
import sys
import logging
import requests
import urllib
import urllib.request
import json
import hmac
import hashlib

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize, URIAction
from linebot.models import CameraAction, CameraRollAction
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage, ImageSendMessage, VideoSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent, FlexSendMessage
)
from linebot.models.actions import PostbackAction

from linebot.exceptions import (LineBotApiError, InvalidSignatureError)
from myqsl.tip_sql import convertAllmessage, history_tip, jason_insert, amount_bill_process_postback, total_amountBill, \
    convertTomessage2
import pymysql.cursors

conn = pymysql.connect(host='myfirstproject.c94g44mqus56.ap-northeast-1.rds.amazonaws.com',
                    user='admin',
                    password = 'D5H3bomrfLKtRW7geo31',
                    db='tip_line_schema',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor)


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# LINEBOTと接続するための記述
# 環境変数からLINEBotのチャンネルアクセストークンとシークレットを読み込む
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# 無いならエラー
if channel_secret is None:
    logger.error('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    logger.error('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

# apiとhandlerの生成（チャンネルアクセストークンとシークレットを渡す）
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

shota_id = "U216e9f3bb4781422a3d3af51e0697dd3"


# Lambdaのメインの動作
def lambda_handler(event, context, amount_bill=None):
    print(event)
    # 認証用のx-line-signatureヘッダー
    signature = event["headers"]["x-line-signature"]
    body = event["body"]

    # リターン値の設定
    ok_json = {"isBase64Encoded": False,
               "statusCode": 200,
               "headers": {},
               "body": ""}
    error_json = {"isBase64Encoded": False,
                  "statusCode": 500,
                  "headers": {},
                  "body": "Error"}


    # 例外処理としての動作
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        logger.error("Got exception from LINE Messaging API: %s\n" % e.handle_message)
        for m in e.error.details:
            logger.error("  %s: %s" % (m.property, m.handle_message))
        return error_json
    except InvalidSignatureError:
        return error_json

    return ok_json


# 以下でWebhookから送られてきたイベントをどのように処理するかを記述する
#各機能のボタン部分を作成
#add handler for rich menu
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    send_message = event.message.text
    print(event)
    display_name = 'None'
    if isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        user_id = event.source.user_id
        display_name = profile.display_name

    else:
        print("user profile can't not use")

    if send_message == "History Tip" and isinstance(event.source, SourceUser):
        print("History Tip")
        tips = history_tip(conn, event.source.user_id)
        print("Tips generated")
        print(tips)
        text = convertAllmessage(tips)
        print("Message converted")
        print(text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text= text))
    elif send_message[:5] == "Bill " and isinstance(event.source, SourceUser):
        # send_message = "Bill 200"
        bill_amount = send_message.replace("Bill ", "")
        # bill_amount = "200"
        if bill_amount.isdigit():
            bubble = jason_insert(bill_amount)

            message = FlexSendMessage(alt_text="Bill sent", contents=bubble)
            line_bot_api.reply_message(
                event.reply_token,
                message
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                (TextSendMessage(text='Invalid bill format. Send Bill again!!'))
            )
    elif send_message[:7] == "Tipped " and isinstance(event.source, SourceUser):
        total_bill = total_amountBill(conn, event.source.user_id)
        print("Tips Generated")
        text2 = convertTomessage2(total_bill)
        print(total_bill)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=text2))
@handler.add(PostbackEvent)
def handle_postback(event,amount_bill):
    if amount_bill_process_postback(event.postback.data,event.source.user_id):

        line_bot_api.reply_message(
                event.reply_token,
                (TextSendMessage(text= "Thank you for your tip"))
        )

# #user add tasks name:
#     elif send_message == user_task and isinstance(event.source, SourceUser):
#
#         message = FlexSendMessage(alt_text="タスクタイプを選択", contents=json.loads(add_task_2))
#         line_bot_api.reply_message(
#             event.reply_token,
#             message
#         )

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='登録して頂きありがとうございます！お会計時に払うTipの料金、払った金額の記録を閲覧できるアカウントです。\n\n下記Menuから使用方法をご覧いただけます。\n\nぜひ旅行の際にご活用頂ければ幸いです。'))

