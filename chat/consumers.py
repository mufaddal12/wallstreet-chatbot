import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from trading.models import *
from django.db import User
from chat.models import *
import random
from chat.utils import *

def IsCompany(company_name):
    company1=Company.objects.filter(name__contains=company_name).first()
    return True if company1 else False

@database_sync_to_async
def create_message(author,text):
    Message.objects.create(author=Profile.objects.get(user__id=author),message=text)


@database_sync_to_async
def add_bidding(user, buy_sell, company, share_bid, share_bid_price):
    pass

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user_id=int(self.room_name.split("_")[0])

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

        buy_sell = text_data_json['buy_sell'] # 0
        company_name=text_data_json['company_name'] # default
        bidding_price=text_data_json['bidding_price'] # -1
        share_count=text_data_json['share_count'] # -1
        

        if buy_sell == 0:
            for i in message.split():
                if i in buy_keywords and buy_sell==0:
                    buy_sell=1
                elif i in sell_keywords and buy_sell==0:
                    buy_sell=-1

        if company_name == "default":
            for i in message.split():
                if IsCompany(i.lower()) and company_name!="default":
                    company_name=Company.objects.filter(name__contains=company_name).first().name


        if buy_sell:
            if company_name != "default":
                if bidding_price != -1 :
                    for i in message.split():
                        try:
                            val = int(i)
                            share_count = val
                            #TODO: add bidding to the database
                            message = "Your bid has been added to the database!"
                        except:
                            message = "Enter proper value!"
                else:
                    for i in message.split():
                        try:
                            val = float(i)
                            bidding_price = val
                            if buy_sell:    
                                message = "How many number of shares do you want to buy?"
                            else:
                                message = "How many number of shares do you want to sell?"
                        except:
                            message = "Enter proper value!"
            else:
                for i in message.split():
                    if IsCompany(i.lower()):
                        company_name=Company.objects.filter(name__contains=company_name).first().name

                if company_name != "default":
                    if buy_sell == 1:
                        message = "What's the price you want to buy the shares at? (price per share)"
                    else:
                        message = "What's the price you want to sell the shares at? (price per share)"
                else:
                    if buy_sell == 1:
                        message = "Which company shares do you want to buy?"
                    else:
                        message = "Which company shares do you want to sell?"
        else:
            for i in message.split():
                if i in buy_keywords and buy_sell==0:
                    buy_sell=1
                elif i in sell_keywords and buy_sell==0:
                    buy_sell=-1
                elif IsCompany(i.lower()) and company_name!="default":
                    company_name=Company.objects.filter(name__contains=company_name).first().name
            if buy_sell == 0:
                message = "Do you want to buy or sell shares?"


        context = {
            "buy_sell":buy_sell,
            "company_name":company_name, 
            "bidding_price":bidding_price,
            "share_count":share_count
        }

        context.update({
                'type': 'chat_message',
                'message': message,
            })

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            context
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))