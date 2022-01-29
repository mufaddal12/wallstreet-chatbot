from django.shortcuts import render


def index(request):
    context={}
    return render(request,'chat/chat.html',context=context)

def room(request):
    username=request.user.id
    context={'room_name':str(username)}
    return render(request,'chat/room.html',context=context)



