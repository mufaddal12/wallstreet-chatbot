import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from trading.models import *
from django.contrib.auth.models import User
from chat.models import *
import random
from chat.utils import *
from trading.matchUtilities import *


@database_sync_to_async
def IsCompany(company_name):
    company1 = Company.objects.filter(name__contains=company_name)
    if company1.count() == 1:
        return company1.first()
    return None


@database_sync_to_async
def create_message(user_id, text):
    Message.objects.create(author=Profile.objects.get(user__id=user_id), message=text)


@database_sync_to_async
def get_admin_id():
    return User.objects.get(is_superuser=True).id


@database_sync_to_async
def add_bidding(user_id, buy_sell, company, share_bid, share_bid_price):
    company1 = Company.objects.get(name__contains=company)
    profile1 = Profile.objects.get(user__id=user_id)
    if buy_sell == 1:
        if (
            0 < share_bid <= 100
            and share_bid_price > 0
            and profile1.cash > 0
            and profile1.cash >= share_bid * share_bid_price * 1.01
        ):
            moneyAlter(profile1, share_bid_price * share_bid, False)  # Subtract money for user
            BuyTable.objects.create(company=company1, profile=profile1, bidShares=share_bid, bidPrice=share_bid_price)
            return True

    else:
        sharesAvailable = UserShareTable.objects.filter(profile=profile1, company=company1).first()
        if sharesAvailable is None:
            sharesAvailable=0
        else:
            sharesAvailable=sharesAvailable.bidShares

        if share_bid_price > 0 and 0 < share_bid <= sharesAvailable:

            u = UserShareTable.objects.filter(
                company=company1, profile=profile1
            ).first()  # Get entry in userShareTable to remove shares
            if share_bid < u.bidShares:
                # Check If selling lesser number of shares than present
                u.bidShares -= share_bid
                u.save()
            elif share_bid == u.bidShares:
                u.delete()
            SellTable.objects.create(company=company1, profile=profile1, bidShares=share_bid, bidPrice=share_bid_price)
            return True

    return False

import traceback
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        self.user_id = int(self.room_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json["message"]

        # create message object for user who sends message
        await create_message(message, int(self.room_name))

        buy_sell = text_data_json["buy_sell"]  # 0
        company_name = text_data_json["company_name"]  # default
        bidding_price = text_data_json["bidding_price"]  # -1
        share_count = text_data_json["share_count"]  # -1

        if buy_sell == 0:
            for i in message.split():
                if i in buy_keywords and buy_sell == 0:
                    buy_sell = 1
                elif i in sell_keywords and buy_sell == 0:
                    buy_sell = -1

        if company_name == "default":
            for i in message.split():
                if await IsCompany(i.lower().capitalize()) and company_name != "default":
                    company_name = Company.objects.filter(name__contains=company_name).first().name

        if buy_sell:
            if company_name != "default":
                if bidding_price != -1:
                    for i in message.split():
                        try:
                            print("IIII", i)
                            val = int(i)
                            print("VAL", val)
                            share_count = val
                            # TODO: add bidding to the database
                            if await add_bidding(int(self.room_name), buy_sell, company_name, share_count, bidding_price):
                                message1 = "Your bid has been added to the database!"
                            else:
                                message1= "Your bid is invalid"
                        except:
                            message1 = "Enter proper value!"
                            print(traceback.format_exc())
                else:
                    for i in message.split():
                        try:
                            val = float(i)
                            bidding_price = val
                            if buy_sell==1:
                                message1 = "How many number of shares do you want to buy?"
                            elif buy_sell==-1:
                                message1 = "How many number of shares do you want to sell?"
                        except:
                            message1 = "Enter proper value!"
            else:
                for i in message.split():
                    print(i)
                    if await IsCompany(i.lower().capitalize()):
                        print(i)
                        company1 = await IsCompany(i.lower().capitalize())
                        if company1 is not None:
                            company_name = company1.name

                if company_name != "default":
                    if buy_sell == 1:
                        message1 = "What's the price you want to buy the shares at? (price per share)"
                    else:
                        message1 = "What's the price you want to sell the shares at? (price per share)"
                else:
                    if buy_sell == 1:
                        message1 = "Which company shares do you want to buy?"
                    else:
                        message1 = "Which company shares do you want to sell?"
        else:
            for i in message.split():
                if i in buy_keywords and buy_sell == 0:
                    buy_sell = 1
                elif i in sell_keywords and buy_sell == 0:
                    buy_sell = -1
                elif await IsCompany(i.lower().capitalize()) and company_name != "default":
                    company_name = Company.objects.filter(name__contains=company_name).first().name
            if buy_sell == 0:
                message1 = "Do you want to buy or sell shares?"

        # create message object for admin for self-generated message
        await create_message(message1, get_admin_id())

        context = {
            "buy_sell": buy_sell,
            "company_name": company_name,
            "bidding_price": bidding_price,
            "share_count": share_count,
        }

        context.update(
            {
                "type": "chat_message",
                "message": message,
                "message1":message1
            }
        )

        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, context)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        buy_sell = event["buy_sell"]
        company_name = event["company_name"]
        bidding_price = event["bidding_price"]
        share_count = event["share_count"]
        message1=event["message1"]

        # Send company_name to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "buy_sell": buy_sell,
                    "company_name": company_name,
                    "bidding_price": bidding_price,
                    "share_count": share_count,
                    "message1":message1
                }
            )
        )
