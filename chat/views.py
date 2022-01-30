from django.shortcuts import render

from chat.models import Message


def index(request):
    context = {}
    return render(request, "chat/chat.html", context=context)


def room(request):
    username = request.user.id
    messages=Message.objects.filter(author__user=request.user)
    context = {
        "room_name": str(username),
        "buy_sell": 0,
        "company_name": "default",
        "bidding_price": -1,
        "share_count": -1,
        "messages":messages,
        "username":request.user.username
        
    }
    return render(request, "chat/room.html", context=context)
