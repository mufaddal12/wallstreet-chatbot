import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from trading.models import *
from django.db import User
from chat.models import *

from chat.utils import *

@database_sync_to_async
def create_message(author,text,BuySell,company_name=None):
    print("AUTHORRR",author)
    author=User.objects.filter(id=author).first()
    profile1=Profile.objects.filter(user=author).first()
    if(company_name):
        company=Company.objects.filter(name__contains=company_name).first()
        if(Message.objects.filter(author=author,message=text)):
            message1=Message.objects.filter(author=author,message=text)
            message1.company=company
            message1.save()
            return message1
        else:    
            message=Message.objects.create(author=profile1,message=text,BuySell=BuySell)
            message.save()
            return message
    
    if(BuySell):
        if(Message.objects.filter(author=author,message=text)):
            message1=Message.objects.filter(author=author,message=text)
            message1.BuySell=BuySell
            message1.save()
            return message1
        else:
            message=Message.objects.create(author=profile1,message=text,BuySell=BuySell)
            message.save()
            return message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user_id=self.room_name.split("_")[0]

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        for i in message:
            if i in buy_keywords:
                message1=await create_message(self.user_id,message,1)
            elif i in sell_keywords:
                message1=await create_message(self.user_id,message,-1)
            elif i in company_name:
                message1=await create_message(self.user_id,message,0,i)
            else:
                message1=await create_message(self.user_id,message,0)


        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))