from django.db import models
from trading.models import *

class Message(models.Model):
    message=models.TextField(max_length=200000,null = True, blank = True, default = "")
    message_time = models.DateTimeField(auto_now_add=True,null=True)
    author=models.ForeignKey(Profile, related_name='message_author', null=True , blank= True, on_delete=models.PROTECT)

    def __str__(self):
        return self.author.user.first_name + ": " + str(self.message)[0:15]