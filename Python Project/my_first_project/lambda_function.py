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
            "align": "center",
            "action": {
              "type": "postback",
              "label": "action",
              "data": "user=taskname",
              "displayText": "Task name"
            }
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
                "cornerRadius": "xxl",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": "most=highest=task",
                  "displayText": "Next task"
                }
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
                "cornerRadius": "xxl",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": "second=highest=task",
                  "displayText": "duolingo"
                }
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
                "cornerRadius": "xxl",
                "action": {
                  "type": "postback",
                  "label": "action",
                  "data": "third=highest=task",
                  "displayText": "upcoming task"
                }
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
                      "data": "add=user=highpriority=task",
                      "displayText": "add task"
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
              "data": "add=user=highpriority=task"
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
                      "data": "add=user=medpriority=task",
                      "displayText": "Add task"
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
              "data": "add=user=medpriority=task"
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
        # user message has to be variable, for now I put some words below.
    elif send_message == "whatever user input" and isinstance(event.source, SourceUser):
        bubble_string = """
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
                "text": "Learn SQL",
                "weight": "bold",
                "color": "#555555",
                "align": "center",
                "size": "xl"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "height": "1px",
                    "backgroundColor": "#aaaaaa",
                    "offsetTop": "7px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "backgroundColor": "#00c300",
                    "height": "3px",
                    "width": "80%",
                    "position": "absolute",
                    "offsetTop": "6px"
                  },
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "10px",
                        "height": "10px",
                        "backgroundColor": "#00c300",
                        "cornerRadius": "5px"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "10px",
                        "height": "10px",
                        "backgroundColor": "#00c300",
                        "cornerRadius": "5px"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "10px",
                        "height": "10px",
                        "backgroundColor": "#00c300",
                        "cornerRadius": "5px"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "10px",
                        "height": "10px",
                        "backgroundColor": "#00c300",
                        "cornerRadius": "5px"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "14px",
                        "height": "14px",
                        "backgroundColor": "#00e600",
                        "cornerRadius": "7px"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "10px",
                        "height": "10px",
                        "backgroundColor": "#aaaaaa",
                        "cornerRadius": "5px"
                      }
                    ],
                    "position": "absolute",
                    "width": "100%",
                    "justifyContent": "space-between",
                    "alignItems": "center"
                  }
                ],
                "height": "14px"
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
                "color": "#555555",
                "wrap": true
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
    """
        message = FlexSendMessage(alt_text="whatever user input", contents=json.loads(bubble_string))
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
#user message has to be variable, for now I put some words below.
    elif send_message == "whatever user input" and isinstance(event.source, SourceUser):
        bubble_string = """
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
            "text": "Learn SQL",
            "weight": "bold",
            "color": "#555555",
            "align": "center",
            "size": "xl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "height": "1px",
                "backgroundColor": "#aaaaaa",
                "offsetTop": "7px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": "#00c300",
                "height": "3px",
                "width": "80%",
                "position": "absolute",
                "offsetTop": "6px"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "10px",
                    "height": "10px",
                    "backgroundColor": "#00c300",
                    "cornerRadius": "5px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "10px",
                    "height": "10px",
                    "backgroundColor": "#00c300",
                    "cornerRadius": "5px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "10px",
                    "height": "10px",
                    "backgroundColor": "#00c300",
                    "cornerRadius": "5px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "10px",
                    "height": "10px",
                    "backgroundColor": "#00c300",
                    "cornerRadius": "5px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "14px",
                    "height": "14px",
                    "backgroundColor": "#00e600",
                    "cornerRadius": "7px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "10px",
                    "height": "10px",
                    "backgroundColor": "#aaaaaa",
                    "cornerRadius": "5px"
                  }
                ],
                "position": "absolute",
                "width": "100%",
                "justifyContent": "space-between",
                "alignItems": "center"
              }
            ],
            "height": "14px"
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
            "color": "#555555",
            "wrap": true
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
"""
        message = FlexSendMessage(alt_text="whatever user input", contents=json.loads(bubble_string))
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
#Function: when user tap action of high priority of "add"
@handler.add(PostbackEvent)
def handle_postback_todo(event):
    if event.postback.data == "add=user=highpriority=task":
        bubble_string = """
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
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "height": "1px",
                "backgroundColor": "#aaaaaa",
                "offsetTop": "7px"
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [],
                "backgroundColor": "#00c300",
                "height": "3px",
                "width": "80%",
                "position": "absolute",
                "offsetTop": "6px"
              },
              {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "10px",
                    "height": "10px",
                    "backgroundColor": "#00c300",
                    "cornerRadius": "5px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "10px",
                    "height": "10px",
                    "backgroundColor": "#00c300",
                    "cornerRadius": "5px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "10px",
                    "height": "10px",
                    "backgroundColor": "#00c300",
                    "cornerRadius": "5px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "10px",
                    "height": "10px",
                    "backgroundColor": "#00c300",
                    "cornerRadius": "5px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "14px",
                    "height": "14px",
                    "backgroundColor": "#00e600",
                    "cornerRadius": "7px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "width": "10px",
                    "height": "10px",
                    "backgroundColor": "#aaaaaa",
                    "cornerRadius": "5px"
                  }
                ],
                "position": "absolute",
                "width": "100%",
                "justifyContent": "space-between",
                "alignItems": "center"
              }
            ],
            "height": "14px"
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
            "color": "#555555",
            "wrap": true
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
        "color": "#aaaaaa",
        "wrap": true
      }
    ],
    "justifyContent": "center",
    "alignItems": "center",
    "paddingTop": "4px"
  }
}
"""
        message = FlexSendMessage(alt_text="add task", contents=json.loads(bubble_string))
        line_bot_api.reply_message(
            event.reply_token,
            message
        )


#when usr tap add of medium priority
    elif event.postback.data == "add=user=medpriority=ask":
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='you are fucking cool'))
        )
    elif event.postback.data == "user=taskname":
        bubble_string = """
{
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Your Tasks",
        "weight": "bold",
        "color": "#1DB446",
        "size": "sm"
      },
      {
        "type": "text",
        "text": "Task name",
        "weight": "bold",
        "size": "xxl",
        "margin": "md",
        "align": "center"
      },
      {
        "type": "separator",
        "margin": "lg"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "sm",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "In Progress",
                    "margin": "xl",
                    "size": "sm",
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
                    "text": "High Priority",
                    "margin": "xl",
                    "size": "sm",
                    "align": "center"
                  }
                ]
              }
            ],
            "margin": "none"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "1 hour 15 minutes Left",
                "size": "sm",
                "color": "#555555",
                "align": "center"
              }
            ],
            "margin": "xl"
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "height": "1px",
                    "backgroundColor": "#aaaaaa",
                    "offsetTop": "7px"
                  },
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "backgroundColor": "#00c300",
                    "height": "3px",
                    "width": "80%",
                    "position": "absolute",
                    "offsetTop": "6px"
                  },
                  {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "10px",
                        "height": "10px",
                        "backgroundColor": "#00c300",
                        "cornerRadius": "5px"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "10px",
                        "height": "10px",
                        "backgroundColor": "#00c300",
                        "cornerRadius": "5px"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "10px",
                        "height": "10px",
                        "backgroundColor": "#00c300",
                        "cornerRadius": "5px"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "10px",
                        "height": "10px",
                        "backgroundColor": "#00c300",
                        "cornerRadius": "5px"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "14px",
                        "height": "14px",
                        "backgroundColor": "#00e600",
                        "cornerRadius": "7px"
                      },
                      {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [],
                        "width": "10px",
                        "height": "10px",
                        "backgroundColor": "#aaaaaa",
                        "cornerRadius": "5px"
                      }
                    ],
                    "position": "absolute",
                    "width": "100%",
                    "justifyContent": "space-between",
                    "alignItems": "center"
                  }
                ],
                "height": "14px"
              }
            ],
            "spacing": "lg"
          },
          {
            "type": "separator",
            "margin": "xxl"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "margin": "xxl",
            "contents": [
              {
                "type": "text",
                "text": "Finish",
                "size": "lg",
                "color": "#555555",
                "align": "center"
              }
            ],
            "backgroundColor": "#00c300",
            "paddingAll": "md",
            "cornerRadius": "xxl",
            "action": {
              "type": "postback",
              "label": "finish action",
              "data": "finish=user=tap",
              "displayText": "Finish Task"
            }
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "Extend Time",
                "size": "sm"
              }
            ],
            "margin": "md"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "20 minutes",
                    "align": "center",
                    "size": "xs"
                  }
                ],
                "action": {
                  "type": "postback",
                  "label": "extend time",
                  "data": "extend=20minutes=task",
                  "displayText": "extend 20 minutes"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "40 minutes",
                    "align": "center",
                    "size": "xs"
                  }
                ],
                "action": {
                  "type": "postback",
                  "label": "extend time",
                  "data": "extend=40minutes=task",
                  "displayText": "extend 40 minutes"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "1 hour",
                    "align": "center",
                    "size": "xs"
                  }
                ],
                "action": {
                  "type": "postback",
                  "label": "extend time",
                  "data": "extend=1hour=task",
                  "displayText": "extend 1 hour"
                }
              }
            ],
            "margin": "lg"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "2 hours",
                    "align": "center",
                    "size": "xs"
                  }
                ],
                "action": {
                  "type": "postback",
                  "label": "extend time",
                  "data": "extend=2hours=task",
                  "displayText": "extend 2 hours"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "Tomorrow",
                    "align": "center",
                    "size": "xs"
                  }
                ],
                "action": {
                  "type": "postback",
                  "label": "extend time",
                  "data": "extend=tomorrow=task",
                  "displayText": "extend due by tomorrow"
                }
              },
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "text",
                    "text": "Next Week",
                    "align": "center",
                    "size": "xs"
                  }
                ],
                "action": {
                  "type": "postback",
                  "label": "extend time",
                  "data": "extend=nextweek=task",
                  "displayText": "extend due by next week"
                }
              }
            ],
            "margin": "lg"
          }
        ]
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "box",
        "layout": "horizontal",
        "margin": "md",
        "contents": [
          {
            "type": "text",
            "text": "Created Today 15:00",
            "size": "xs",
            "color": "#aaaaaa",
            "flex": 0
          },
          {
            "type": "text",
            "text": "Posted Today",
            "color": "#aaaaaa",
            "size": "xs",
            "align": "end"
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
}
"""
        message2 = FlexSendMessage(alt_text="Programming", contents=json.loads(bubble_string))
        line_bot_api.reply_message(
            event.reply_token,
            message2
        )
    elif event.postback.data =="most=highest=task":
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='task name'))
        )
    elif event.postback.data == "second=highest=task":
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='task name 2'))
        )
    elif event.postback.data == "third=highest=task":
        line_bot_api.reply_message(
            event.reply_token,
            (TextSendMessage(text='task name 3'))
        )


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='登録して頂きありがとうございます！Cafe BORCELLEのLINE公式アカウントです。\n\n下記Menuから今日のドリンクメニューやクーポン、お問い合わせ、ホームページのリンクがご確認頂けます。\n\n自動会話botと連携しており、チャットで話しかけると返答が返ってきます。\n\nぜひご活用頂ければ幸いです。'))

