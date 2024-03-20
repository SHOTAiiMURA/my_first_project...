# Complete Gradation
COLOR_DICT = {'a': '#e55b5b', 'b': '#e57b5b', 'c': '#e59b5b', 'd': '#e5bb5b', 'e': '#d6cc55', 'f': '#b9cc51',
              'g': '#93bf4c', 'h': '#78bf4c', 'i': '#5ebf4c', 'j': '#4cbf55', 'k': '#4cbf6f', 'l': '#4cbf8a',
              'm': '#4cbfa4',
              'n': '#5be5e5', 'o': '#5bc5e5', 'p': '#5ba5e5', 'q': '#5b86e5', 'r': '#5b66e5', 's': '#705be5',
              't': '#905be5', 'u': '#b05be5', 'v': '#d05be5', 'w': '#e55bda', 'x': '#e55bbb', 'y': '#e55b9b',
              'z': '#e55b7b'}
# GH Brighten 2 Shift
COLOR_DICT = {'a': '#e55b5b', 'b': '#e59b5b', 'c': '#e5da5b', 'd': '#b0e55b', 'e': '#69d655', 'f': '#51cc77',
              'g': '#51ccaf', 'h': '#51afcc', 'i': '#4c6fbf', 'j': '#5e4cbf', 'k': '#934cbf', 'l': '#bf4cb6',
              'm': '#bf4c81',
              'n': '#e55b5b', 'o': '#e59b5b', 'p': '#e5da5b', 'q': '#b0e55b', 'r': '#70e55b', 's': '#5be586',
              't': '#5be5c5', 'u': '#5bc5e5', 'v': '#5b86e5', 'w': '#705be5', 'x': '#b05be5', 'y': '#e55bda',
              'z': '#e55b9b'}
# GH Brighten
COLOR_DICT = {'a': '#e55b5b', 'b': '#e57b5b', 'c': '#e59b5b', 'd': '#e5bb5b', 'e': '#d6cc55', 'f': '#b9cc51',
              'g': '#9ccc51', 'h': '#80cc51', 'i': '#5ebf4c', 'j': '#4cbf55', 'k': '#4cbf6f', 'l': '#4cbf8a',
              'm': '#4cbfa4',
              'n': '#5be5e5', 'o': '#5bc5e5', 'p': '#5ba5e5', 'q': '#5b86e5', 'r': '#5b66e5', 's': '#705be5',
              't': '#905be5', 'u': '#b05be5', 'v': '#d05be5', 'w': '#e55bda', 'x': '#e55bbb', 'y': '#e55b9b',
              'z': '#e55b7b'}


def drop_shadow(code):
    if len(code) != 7:
        raise ValueError("Hex Code Error : " + hex)
    return "#" + format(int(code[1:3], 16) // 2, '02x') + format(int(code[3:5], 16) // 2, '02x') + format(
        int(code[5:7], 16) // 2, '02x')


def color_variable(code, per):
    if len(code) != 7:
        raise ValueError("Hex Code Error : " + hex)
    return "#" + format(min(int(int(code[1:3], 16) / 100 * per), 255), '02x') + format(
        min(int(int(code[3:5], 16) / 100 * per), 255), '02x') + format(min(int(int(code[5:7], 16) / 100 * per), 255),
                                                                       '02x')


def CustomButton(text, flex=1, text_size="md", command_type="postback", command=None, command_prefix=None,
                 adjust_color=100, color=None, letter_shift=0, height=50, width=None, shadow=False, shadow_distance=6,
                 rounded=False, corner_radius=10, absolute=False, notification=True, disable=False):
    if text is None:
        raise ValueError("Empty Value is not Allowed!")

    if not shadow:
        shadow_distance = 0

    if color is None:
        color = COLOR_DICT[text[0 + letter_shift].lower()]
    if adjust_color != 100:
        color = color_variable(color, adjust_color * 0.8 if color == '#d6cc55' else adjust_color)
    if rounded:
        corner_radius = height // 2

    button = {
        "type": "box",
        "layout": "vertical",
        "flex": flex,
        "position": "absolute" if absolute else "relative",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "height": str(height) + "px",
                "cornerRadius": str(corner_radius) + "px",
                "offsetTop": str(shadow_distance) + "px",
                "backgroundColor": drop_shadow(color)
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # {
                    # "type": "box",
                    # "layout": "horizontal",
                    # "contents": [
                    {
                        "type": "text",
                        "text": text,
                        "color": "#FFFFFF",
                        "flex": 11,
                        "gravity": "center",
                        "align": "center",
                        "weight": "bold",
                        "wrap": True,
                        "maxLines": 2,
                        "size": text_size
                    }
                    #   ,
                    #   {
                    #     "type": "text",
                    #     "text": ">",
                    #     "color": "#FFFFFF",
                    #     "flex": 1,
                    #     "gravity": "center",
                    #     "align": "start",
                    #     "weight": "bold"
                    #   }
                    # ]
                    # }
                ],
                "height": str(height) + "px",
                "cornerRadius": str(corner_radius) + "px",
                "backgroundColor": color,
                "offsetTop": "-" + str(height) + "px",
                "justifyContent": "center"
            }
        ],
        "height": str(height + shadow_distance) + "px"
    }
    if command_type == "postback":
        button["action"] = {
            "type": "postback",
            "label": "action",
            "data": command if command is not None else command_prefix + text if command_prefix is not None else text,
            "displayText": text
        }
    elif command_type == "message":
        button["action"] = {
            "type": "message",
            "label": command,
            "text": command if command is not None else command_prefix + text if command_prefix is not None else text,
        }
    elif command_type == "uri":
        if command[:4] != "http":
            raise ValueError("Invalid URI : " + str(
                command) + "\nCommand argument takes URI and URI should be starting with https or http")
        button["action"] = {
            "type": "uri",
            "label": "action",
            "text": command,
        }
    elif command_type is not None:
        raise ValueError("Command type should be one of message, postback or uri")

    if not notification:
        button["action"].pop("displayText")

    if width is not None:
        button["width"] = str(width) + "px"

    if disable:
        button.pop("action")
    return button


def MonoRoundedButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "Mono Color",
                "color": "#FFFFFF",
                "weight": "bold"
            }
        ],
        "height": "50px",
        "alignItems": "center",
        "justifyContent": "center",
        "cornerRadius": "25px",
        "backgroundColor": "#E9546B"
    }


def MonoRoundedLineButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Mono Rounded Line",
                        "color": "#FFFFFF",
                        "weight": "bold"
                    }
                ],
                "justifyContent": "center",
                "alignItems": "center",
                "borderColor": "#FFFFFF",
                "borderWidth": "1px",
                "paddingAll": "20px",
                "width": "250px",
                "cornerRadius": "40px",
                "height": "40px"
            }
        ],
        "alignItems": "center",
        "justifyContent": "center",
        "height": "50px",
        "cornerRadius": "50px",
        "backgroundColor": "#EA5532"
    }


def LineButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Line",
                        "color": "#FFFFFF",
                        "weight": "bold"
                    }
                ],
                "justifyContent": "center",
                "alignItems": "center",
                "borderColor": "#FFFFFF",
                "borderWidth": "1px",
                "paddingAll": "20px",
                "width": "250px",
                "cornerRadius": "8px",
                "height": "40px"
            }
        ],
        "alignItems": "center",
        "justifyContent": "center",
        "height": "50px",
        "cornerRadius": "10px",
        "backgroundColor": "#F6AD3C"
    }


def LineWhiteBGButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "White BG Color Line",
                        "color": "#AACF52",
                        "weight": "bold"
                    }
                ],
                "justifyContent": "center",
                "alignItems": "center",
                "borderColor": "#AACF52",
                "borderWidth": "1px",
                "paddingAll": "20px",
                "width": "250px",
                "cornerRadius": "8px",
                "height": "40px"
            }
        ],
        "alignItems": "center",
        "justifyContent": "center",
        "height": "50px",
        "cornerRadius": "10px",
        "borderColor": "#AACF52",
        "borderWidth": "1px"
    }


def ShadowButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "Shadow",
                "color": "#FFFFFF",
                "flex": 1,
                "gravity": "center",
                "align": "center",
                "weight": "bold"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "height": "6px",
                "backgroundColor": "#008048",
                "flex": 0
            }
        ],
        "height": "50px",
        "cornerRadius": "10px",
        "backgroundColor": "#00A95F"
    }


def ShadowArrowButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "Shadow Arrow",
                        "color": "#FFFFFF",
                        "flex": 1,
                        "gravity": "center",
                        "align": "center",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": ">",
                        "color": "#FFFFFF",
                        "flex": 0,
                        "gravity": "center",
                        "align": "end",
                        "weight": "bold",
                        "offsetEnd": "10px"
                    }
                ],
                "flex": 1
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "height": "6px",
                "backgroundColor": "#00807e",
                "flex": 0
            }
        ],
        "height": "50px",
        "cornerRadius": "10px",
        "backgroundColor": "#00ADA9"
    }


def DoubleLineButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Double Line",
                        "color": "#FFFFFF",
                        "gravity": "center",
                        "align": "center",
                        "weight": "bold"
                    }
                ],
                "borderColor": "#00807e",
                "borderWidth": "2px",
                "width": "245px",
                "cornerRadius": "7px",
                "height": "35px",
                "justifyContent": "center",
                "alignItems": "center"
            }
        ],
        "alignItems": "center",
        "height": "50px",
        "cornerRadius": "10px",
        "backgroundColor": "#00AFEC",
        "borderColor": "#00807e",
        "borderWidth": "3px",
        "justifyContent": "center"
    }


def InsetButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Inset Button",
                        "color": "#FFFFFF",
                        "weight": "bold"
                    }
                ],
                "justifyContent": "center",
                "alignItems": "center",
                "width": "245px",
                "cornerRadius": "2px",
                "height": "38px",
                "background": {
                    "type": "linearGradient",
                    "angle": "352deg",
                    "startColor": "#1884cc",
                    "endColor": "#1574b3"
                }
            }
        ],
        "alignItems": "center",
        "justifyContent": "center",
        "height": "50px",
        "cornerRadius": "3px",
        "background": {
            "type": "linearGradient",
            "angle": "352deg",
            "startColor": "#1574b3",
            "endColor": "#0c4266",
            "centerColor": "#1574b3",
            "centerPosition": "20%"
        },
        "paddingTop": "1px",
        "paddingStart": "1px"
    }


def OutsetButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Outset Button",
                        "color": "#FFFFFF",
                        "weight": "bold"
                    }
                ],
                "width": "245px",
                "height": "38px",
                "justifyContent": "center",
                "alignItems": "center",
                "cornerRadius": "2px",
                "backgroundColor": "#A64A97",
                "background": {
                    "type": "linearGradient",
                    "angle": "352deg",
                    "startColor": "#A64A97",
                    "endColor": "#99458b"
                }
            }
        ],
        "height": "50px",
        "alignItems": "center",
        "justifyContent": "center",
        "cornerRadius": "3px",
        "backgroundColor": "#4D4398",
        "background": {
            "type": "linearGradient",
            "angle": "172deg",
            "startColor": "#99458b",
            "endColor": "#662e5d"
        },
        "paddingTop": "1px",
        "paddingStart": "1px"
    }


def GradationButton_2():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "2 Color Gradation",
                "color": "#FFFFFF",
                "weight": "bold"
            }
        ],
        "height": "50px",
        "alignItems": "center",
        "justifyContent": "center",
        "cornerRadius": "25px",
        "backgroundColor": "#E9546B",
        "background": {
            "type": "linearGradient",
            "angle": "90deg",
            "startColor": "#E9546B",
            "endColor": "#F6AD3C"
        }
    }


def GradationButton_3():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "3 Color Gradation Rounded ",
                        "color": "#FFFFFF",
                        "weight": "bold"
                    }
                ],
                "justifyContent": "center",
                "alignItems": "center",
                "borderColor": "#FFFFFF",
                "borderWidth": "1px",
                "paddingAll": "20px",
                "width": "250px",
                "cornerRadius": "40px",
                "height": "40px"
            }
        ],
        "alignItems": "center",
        "justifyContent": "center",
        "height": "50px",
        "cornerRadius": "50px",
        "backgroundColor": "#EA5532",
        "background": {
            "type": "linearGradient",
            "angle": "270deg",
            "startColor": "#00A95F",
            "endColor": "#E9546B",
            "centerColor": "#F6AD3C"
        }
    }


def GradationShadowButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "Gradation shadow",
                "color": "#FFFFFF",
                "weight": "bold"
            }
        ],
        "alignItems": "center",
        "justifyContent": "center",
        "height": "50px",
        "cornerRadius": "10px",
        "backgroundColor": "#F6AD3C",
        "background": {
            "type": "linearGradient",
            "angle": "180deg",
            "startColor": "#e6cf37",
            "endColor": "#d98934",
            "centerColor": "#F6AD3C"
        }
    }


def GradationColorShadowButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "Gradation color shadow",
                "color": "#AACF52",
                "weight": "bold"
            }
        ],
        "alignItems": "center",
        "justifyContent": "center",
        "height": "50px",
        "cornerRadius": "10px",
        "borderColor": "#AACF52",
        "borderWidth": "1px",
        "background": {
            "type": "linearGradient",
            "angle": "180deg",
            "startColor": "#FFFFFFFF",
            "endColor": "#AACF52FF"
        }
    }


def MonotoneShadowButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "Monotone shadow",
                "color": "#777777",
                "flex": 1,
                "gravity": "center",
                "align": "center",
                "weight": "bold"
            }
        ],
        "height": "50px",
        "cornerRadius": "10px",
        "backgroundColor": "#00A95F",
        "background": {
            "type": "linearGradient",
            "angle": "180deg",
            "endColor": "#aaaaaa",
            "startColor": "#efefef",
            "centerColor": "#ffffff"
        }
    }


def GradationDropShadowButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                        "type": "text",
                        "text": "Gradation & drop shadow",
                        "color": "#FFFFFF",
                        "flex": 1,
                        "gravity": "center",
                        "align": "center",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": ">",
                        "color": "#FFFFFF",
                        "flex": 0,
                        "gravity": "center",
                        "align": "end",
                        "weight": "bold",
                        "offsetEnd": "10px"
                    }
                ],
                "flex": 1
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "height": "6px",
                "backgroundColor": "#00807e",
                "flex": 0
            }
        ],
        "height": "50px",
        "cornerRadius": "10px",
        "backgroundColor": "#00ADA9",
        "background": {
            "type": "linearGradient",
            "angle": "180deg",
            "startColor": "#00ADA9",
            "endColor": "#009996",
            "centerColor": "#00bfbc"
        }
    }


def LineGradationButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Line Gradation",
                        "color": "#FFFFFF",
                        "weight": "bold"
                    }
                ],
                "width": "250px",
                "height": "42px",
                "justifyContent": "center",
                "alignItems": "center",
                "cornerRadius": "4px",
                "backgroundColor": "#0c4266",
                "background": {
                    "type": "linearGradient",
                    "angle": "352deg",
                    "startColor": "#09324d",
                    "endColor": "#09324d",
                    "centerColor": "#0c4266"
                }
            }
        ],
        "height": "50px",
        "alignItems": "center",
        "justifyContent": "center",
        "cornerRadius": "6px",
        "backgroundColor": "#4D4398",
        "background": {
            "type": "linearGradient",
            "angle": "172deg",
            "endColor": "#00ccff",
            "startColor": "#d400d4",
            "centerColor": "#0c4266"
        },
        "paddingTop": "1px",
        "paddingStart": "1px"
    }


def SphereButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "Sphere",
                "color": "#888888",
                "gravity": "center",
                "align": "center",
                "weight": "bold"
            }
        ],
        "alignItems": "center",
        "height": "108px",
        "cornerRadius": "54px",
        "backgroundColor": "#00AFEC",
        "justifyContent": "center",
        "width": "108px",
        "background": {
            "type": "linearGradient",
            "angle": "180deg",
            "startColor": "#efefef",
            "centerColor": "#ffffff",
            "endColor": "#aaaaaa"
        }
    }


def MonoCircleButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "text",
                "text": "Mono Circle",
                "color": "#FFFFFF",
                "weight": "bold"
            }
        ],
        "height": "108px",
        "alignItems": "center",
        "justifyContent": "center",
        "cornerRadius": "54px",
        "backgroundColor": "#E9546B",
        "width": "108px"
    }


def LineCircleButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Line Circle",
                        "color": "#FFFFFF",
                        "weight": "bold",
                        "wrap": True,
                        "align": "center"
                    }
                ],
                "justifyContent": "center",
                "alignItems": "center",
                "borderColor": "#FFFFFF",
                "borderWidth": "1px",
                "paddingAll": "20px",
                "width": "98px",
                "cornerRadius": "49px",
                "height": "98px"
            }
        ],
        "alignItems": "center",
        "justifyContent": "center",
        "height": "108px",
        "cornerRadius": "54px",
        "backgroundColor": "#EA5532",
        "width": "108px"
    }


def CircleShadowButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "height": "108px",
                "cornerRadius": "54px",
                "backgroundColor": "#008048",
                "width": "108px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Shadow",
                        "color": "#FFFFFF",
                        "flex": 1,
                        "gravity": "center",
                        "align": "center",
                        "weight": "bold"
                    }
                ],
                "height": "108px",
                "cornerRadius": "54px",
                "backgroundColor": "#00A95F",
                "width": "108px",
                "offsetTop": "-114px"
            }
        ],
        "height": "108px",
        "cornerRadius": "54px",
        "backgroundColor": "#00A95F",
        "width": "108px"
    }


def CircleShadowArrowButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "height": "108px",
                "cornerRadius": "54px",
                "backgroundColor": "#00807e",
                "width": "108px"
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
                                "type": "text",
                                "text": "Shadow & Arrow",
                                "color": "#FFFFFF",
                                "flex": 1,
                                "gravity": "center",
                                "align": "center",
                                "weight": "bold",
                                "margin": "lg",
                                "wrap": True
                            },
                            {
                                "type": "text",
                                "color": "#FFFFFF",
                                "flex": 0,
                                "gravity": "bottom",
                                "align": "center",
                                "weight": "bold",
                                "text": "▼",
                                "offsetBottom": "10px",
                                "size": "lg"
                            }
                        ],
                        "flex": 1
                    }
                ],
                "height": "108px",
                "cornerRadius": "54px",
                "backgroundColor": "#00ADA9",
                "width": "108px",
                "offsetTop": "-114px"
            }
        ],
        "height": "108px",
        "cornerRadius": "54px",
        "backgroundColor": "#00ADA9",
        "width": "108px"
    }


def UpButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "backgroundColor": "#DDDDDD",
                "width": "50px",
                "height": "50px",
                "cornerRadius": "25px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "↑",
                        "align": "center",
                        "gravity": "center",
                        "color": "#444444",
                        "size": "xl"
                    }
                ],
                "backgroundColor": "#FFFFFF",
                "width": "50px",
                "height": "50px",
                "cornerRadius": "25px",
                "offsetTop": "-54px",
                "alignItems": "center",
                "justifyContent": "center"
            }
        ],
        "paddingTop": "4px"
    }


def DownButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "backgroundColor": "#DDDDDD",
                "width": "50px",
                "height": "50px",
                "cornerRadius": "25px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "↓",
                        "align": "center",
                        "gravity": "center",
                        "color": "#444444",
                        "size": "xl"
                    }
                ],
                "backgroundColor": "#FFFFFF",
                "width": "50px",
                "height": "50px",
                "cornerRadius": "25px",
                "offsetTop": "-54px",
                "alignItems": "center",
                "justifyContent": "center"
            }
        ],
        "paddingTop": "4px"
    }


def LeftButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "backgroundColor": "#DDDDDD",
                "width": "50px",
                "height": "50px",
                "cornerRadius": "25px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "←",
                        "align": "center",
                        "gravity": "center",
                        "color": "#444444",
                        "size": "xl"
                    }
                ],
                "backgroundColor": "#FFFFFF",
                "width": "50px",
                "height": "50px",
                "cornerRadius": "25px",
                "offsetTop": "-54px",
                "justifyContent": "center"
            }
        ],
        "paddingTop": "4px"
    }


def RightButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "backgroundColor": "#DDDDDD",
                "width": "50px",
                "height": "50px",
                "cornerRadius": "25px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "→",
                        "align": "center",
                        "gravity": "center",
                        "color": "#444444",
                        "size": "xl"
                    }
                ],
                "backgroundColor": "#FFFFFF",
                "width": "50px",
                "height": "50px",
                "cornerRadius": "25px",
                "offsetTop": "-54px",
                "justifyContent": "center"
            }
        ],
        "paddingTop": "4px"
    }


def RewindButton():
    return {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "filler"
                    }
                ],
                "backgroundColor": "#DDDDDD",
                "width": "50px",
                "height": "50px",
                "cornerRadius": "25px"
            },
            {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "⟳",
                        "align": "center",
                        "gravity": "center",
                        "color": "#444444",
                        "size": "xl"
                    }
                ],
                "backgroundColor": "#FFFFFF",
                "width": "50px",
                "height": "50px",
                "cornerRadius": "25px",
                "offsetTop": "-54px",
                "justifyContent": "center"
            }
        ],
        "paddingTop": "4px"
    }
