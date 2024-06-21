import os
from dotenv import load_dotenv
from botbuilder.core import BotFrameworkAdapter, TurnContext, MessageFactory
from botbuilder.schema import Activity, ActivityTypes
from aiohttp import web

load_dotenv()

APP_ID = os.getenv("MICROSOFT_APP_ID")
APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD")

# Bot ke message handler function ko define karna
async def on_message_activity(turn_context: TurnContext):
    await turn_context.send_activity(Activity(type=ActivityTypes.message, text="Hello! This is your bot speaking."))

# Notification bhejne ke liye function
async def send_notification(adapter: BotFrameworkAdapter, recipient_id: str):
    message = MessageFactory.text("This is a notification.")
    conversation_reference = {
        'serviceUrl': "https://smba.trafficmanager.net/apis/",
        'channelId': "skype",
        'conversation': {
            'id': recipient_id
        },
        'user': {
            'id': recipient_id
        }
    }
    await adapter.continue_conversation(conversation_reference, lambda turn_context: turn_context.send_activity(message), APP_ID)

# Bot adapter aur HTTP server setup karna
adapter = BotFrameworkAdapter(APP_ID, APP_PASSWORD)

async def messages(req):
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get('Authorization', '')
    response = await adapter.process_activity(activity, auth_header, on_message_activity)
    return web.json_response(response.body, status=response.status)

app = web.Application()
app.router.add_post('/api/messages', messages)

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=3978)
