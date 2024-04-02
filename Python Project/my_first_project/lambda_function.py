import os
import sys
import logging
import requests
import urllib
import urllib.request
import json

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
def lambda_handler(event, context):
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

    if send_message == "Add" and isinstance(event.source, SourceUser):
        add_task_1 = """
        {
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
            "text": "New Task",
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
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Type task name below",
            "size": "xl",
            "color": "#555555"
          },
          {
            "type": "text",
            "text": "Ex) learn SQL",
            "color": "#aaaaaa"
          }
        ],
        "spacing": "md"
      }
    ],
    "spacing": "xl"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Input with Keyboard",
        "color": "#aaaaaa"
      }
    ],
    "justifyContent": "center",
    "alignItems": "center",
    "paddingTop": "4px"
  }
}
"""
        message = FlexSendMessage(alt_text="タスクを追加する", contents=json.loads(add_task_1))
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif send_message == "Programming" and isinstance(event.source, SourceUser):
        add_task_2 =[
            {
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
            "text": "Programming",
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
            "text": "Choose Task Type",
            "size": "xl",
            "color": "#555555"
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
            "text": "Duration + Due",
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
          "label": "Duration and Due",
          "data": "DurationDue=User=tap",
          "displayText": "Choose duration and due of task"
        }
      },
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "type": "text",
            "text": "Duration",
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
          "label": "Duration of task",
          "data": "Duration=usr=task",
          "displayText": "Choose duration of your task"
        }
      },
      {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Start + End",
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
          "label": "Start time and end time",
          "data": "Start&end=user=tap",
          "displayText": "Choose starting time and end time"
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
]
        message = FlexSendMessage(alt_text="タスクタイプを選択", contents=json.loads(add_task_2))
        line_bot_api.reply_message(
            event.reply_token,
            message
        )

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='登録して頂きありがとうございます！Cafe BORCELLEのLINE公式アカウントです。\n\n下記Menuから今日のドリンクメニューやクーポン、お問い合わせ、ホームページのリンクがご確認頂けます。\n\n自動会話botと連携しており、チャットで話しかけると返答が返ってきます。\n\nぜひご活用頂ければ幸いです。'))

