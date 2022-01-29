import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from trading.models import *
from django.db import User
from chat.models import *

from chat.utils import *

def IsCompany(company_name):
    company1=Company.objects.filter(name__contains=company_name).first()
    return True if company1 else False

@database_sync_to_async
def create_message(author,text,BuySell=0,company_name=None):
    print("AUTHORRR",author)
    author=User.objects.filter(id=author).first()
    profile1=Profile.objects.filter(user=author).first()
    if(company_name):
        company=Company.objects.filter(name__contains=company_name).first()
        if(Message.objects.filter(author=author,message=text)):
            message1=Message.objects.filter(author=author,message=text).first()
            message1.company=company
            message1.save()
            return message1
        else:    
            message=Message.objects.create(author=profile1,message=text,BuySell=BuySell,company=company)
            message.save()
            return message
    
    if(BuySell):
        if(Message.objects.filter(author=author,message=text)):
            message1=Message.objects.filter(author=author,message=text).first()
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
        buy_sell = text_data_json['buy_sell']
        company_name=text_data_json['company_name']
        bidding_price=text_data_json['bidding_price']
        share_count=text_data_json['share_count']
        

        for i in message.split():
            if i in buy_keywords and buy_sell==0:
                buy_sell=1
                # message1=await create_message(self.user_id,message,1)
            elif i in sell_keywords and buy_sell==0:
                buy_sell=-1
                # message1=await create_message(self.user_id,message,-1)
            elif IsCompany(i.lower()) and company_name!="default":
                # message1=await create_message(self.user_id,message,0,i.lower())
                company_name=Company.objects.filter(name__contains=company_name).first().name
            elif i==-1:
                message1=await create_message(self.user_id,message,0)

        if message1.BuySell!=0:
            if message1.company is not None:
                message2="Please mention the number of stocks and your bidding amount"
                await create_message(admin_user,message2)
            else:
                message2="Please mention comp"


        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message2':message2

            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))