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

keita_id = "Ucf4318317d8fbc721674ae755d49b3cb"


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

    if send_message == "View" and isinstance(event.source, SourceUser):
        bubble_string = """
        {
  "type": "carousel",
  "contents": [
  {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "In Progress",
        "weight": "bold",
        "color": "#1DB446",
        "size": "sm"
      },
      {
        "type": "text",
        "text": "Task name",
        "weight": "bold",
        "size": "xxl",
        "margin": "sm",
        "align": "center"
      },
      {
        "type": "text",
        "text": "Remaining X minutes...",
        "size": "xxs",
        "color": "#aaaaaa",
        "wrap": true,
        "align": "center"
      },
      {
        "type": "separator",
        "margin": "lg"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "md",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "Next Task",
                "size": "sm",
                "color": "#1DB446",
                "weight": "bold"
              }
            ],
            "margin": "none"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "duolingo",
                "size": "xxl",
                "color": "#555555",
                "align": "center"
              },
              {
                "type": "text",
                "text": "Starts in 10 minuties",
                "size": "xxs",
                "align": "center"
              }
            ],
            "margin": "xs"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "Upcoming Tasks",
                "size": "sm",
                "color": "#1DB446",
                "weight": "bold",
                "margin": "none"
              }
            ],
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Task4",
                "size": "lg",
                "color": "#555555",
                "align": "center"
              },
              {
                "type": "text",
                "text": "Starts in 30 minutes",
                "size": "xxs",
                "color": "#111111",
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Tasks 5",
                "size": "lg",
                "color": "#555555",
                "align": "center"
              },
              {
                "type": "text",
                "text": "Starts in 40 minutes",
                "size": "xxs",
                "color": "#111111",
                "align": "center"
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Tasks 6",
                "size": "lg",
                "color": "#555555",
                "align": "center"
              },
              {
                "type": "text",
                "text": "Starts in 50 minutes",
                "size": "xxs",
                "color": "#111111",
                "align": "center"
              }
            ]
          }
        ]
      },
      {
        "type": "separator",
        "margin": "xl"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "3.20.2024",
            "size": "xs",
            "color": "#aaaaaa",
            "flex": 0
          }
        ]
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": true
    }
  }
},
{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "High Priority",
        "weight": "bold",
        "color": "#1DB446",
        "size": "xxl",
        "align": "center"
      },
      {
        "type": "separator",
        "margin": "sm"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "md",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Next Task",
                "size": "xl",
                "color": "#555555",
                "align": "center"
              },
              {
                "type": "text",
                "text": "hello, world",
                "size": "xxs",
                "align": "center"
              }
            ],
            "margin": "xs",
            "backgroundColor": "#aaaaaa",
            "cornerRadius": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "duolingo",
                "size": "xl",
                "color": "#555555",
                "align": "center"
              },
              {
                "type": "text",
                "text": "Starts in 10 minuties",
                "size": "xxs",
                "align": "center"
              }
            ],
            "margin": "md",
            "backgroundColor": "#aaaaaa",
            "cornerRadius": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Upcoming Tasks",
                "size": "lg",
                "color": "#555555",
                "align": "center"
              },
              {
                "type": "text",
                "text": "hello, world",
                "align": "center",
                "size": "xxs"
              }
            ],
            "margin": "md",
            "backgroundColor": "#aaaaaa",
            "cornerRadius": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "Add Task",
                  "data": "hello",
                  "displayText": "Hellomotherfucker"
                }
              }
            ],
            "margin": "xxl",
            "cornerRadius": "xxl",
            "backgroundColor": "#1DB446",
            "justifyContent": "space-between",
            "alignItems": "center"
          }
        ],
        "action": {
          "type": "postback",
          "label": "action",
          "data": "hello"
        }
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": true
    }
  }
},
{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Medium Priority",
        "weight": "bold",
        "color": "#1DB446",
        "size": "xxl",
        "align": "center"
      },
      {
        "type": "separator",
        "margin": "sm"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "md",
        "contents": [
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Next Task",
                "size": "xl",
                "color": "#555555",
                "align": "center"
              },
              {
                "type": "text",
                "text": "hello, world",
                "size": "xxs",
                "align": "center"
              }
            ],
            "margin": "xs",
            "backgroundColor": "#aaaaaa",
            "cornerRadius": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "duolingo",
                "size": "xl",
                "color": "#555555",
                "align": "center"
              },
              {
                "type": "text",
                "text": "Starts in 10 minuties",
                "size": "xxs",
                "align": "center"
              }
            ],
            "margin": "md",
            "backgroundColor": "#aaaaaa",
            "cornerRadius": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "text",
                "text": "Upcoming Tasks",
                "size": "lg",
                "color": "#555555",
                "align": "center"
              },
              {
                "type": "text",
                "text": "hello, world",
                "align": "center",
                "size": "xxs"
              }
            ],
            "margin": "md",
            "backgroundColor": "#aaaaaa",
            "cornerRadius": "xxl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "button",
                "action": {
                  "type": "postback",
                  "label": "Add Task",
                  "data": "hello2",
                  "displayText": "Hellomotherfucker"
                }
              }
            ],
            "margin": "xxl",
            "cornerRadius": "xxl",
            "backgroundColor": "#1DB446",
            "justifyContent": "space-between",
            "alignItems": "center"
          }
        ],
        "action": {
          "type": "postback",
          "label": "action",
          "data": "hello"
        }
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": true
    }
  }
}
  ]
}
"""
        message = FlexSendMessage(alt_text="View", contents=json.loads(bubble_string))
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif send_message == "Add" and isinstance(event.source, SourceUser):
        profile = line_bot_api.get_profile(event.source.user_id)
        tmpname = profile.display_name
        line_bot_api.reply_message(
            event.reply_token,
            (ImageSendMessage(
                original_content_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/cafe_menu.png",
                preview_image_url="https://maindepository.s3.ap-northeast-1.amazonaws.com/cafe_menu.png")))

#Function: when user tap action of high priority
@handler.add(PostbackEvent)
def handle_postback_todo(event):
    if event.todo.data == "hello":
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='you are awesome!!'))
        )
    elif event.todo.data == "hello2":
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='you are fucking cool'))
        )

#Function: when user tap action button of medium priority
@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'action=question&id=1':
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='平日は8:30~17:00、祝休日は8:30~21:00まで開いています。'))
        )
    elif event.postback.data == 'action=question&id=2':
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='下記リンクからGoogle Mapで確認できます。\nhttps://goo.gl/maps/m2KbyY6RA8QepLaa8'))
        )
    elif event.postback.data == 'action=question&id=3':
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='はい、車6台が停めれる駐車場がございます。また、駐輪場もございます。'))
        )
    elif event.postback.data == 'action=question&id=4':
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='申し訳ございません。デリバリーもテイクアウトも今はやっておりません'))
        )

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='登録して頂きありがとうございます！Cafe BORCELLEのLINE公式アカウントです。\n\n下記Menuから今日のドリンクメニューやクーポン、お問い合わせ、ホームページのリンクがご確認頂けます。\n\n自動会話botと連携しており、チャットで話しかけると返答が返ってきます。\n\nぜひご活用頂ければ幸いです。'))
