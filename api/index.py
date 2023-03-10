from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT

import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

# domain root
@app.route('/')
def home():
    return 'Hello, World'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    
    # get request body as text
    body = request.get_data(as_text=True)
    
    app.logger.info("Request body: " + body)
    
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
        
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    
    if event.message.type != "text":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Not supported input"))
        return
    
    if event.message.text == "on":
        working_status = True
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="1234"))
        return

    if event.message.text == "off":
        working_status = False
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="4567"))
        return
    
    if working_status:
        reply_msg = chatgpt.get_response(event.message.text)
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=type(event.message.text)))


if __name__ == "__main__":
    app.run()
