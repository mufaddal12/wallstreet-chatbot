from django.db import models
from trading.models import *

class Message(models.Model):
    message=models.TextField(max_length=200000,null = True, blank = True, default = "")
    message_time = models.DateTimeField(auto_now_add=True,null=True)
    author=models.ForeignKey(Profile, related_name='message_author', null=True , blank= True, on_delete=models.PROTECT)
    BuySell=models.BooleanField(null = True, default = False)
    CompanyAction=models.BooleanField(null = True, default = False)
    Company=models.ForeignKey(Company, related_name='message_company', on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return str(self.message)[0:15]