from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime

# User share table and User history - Improve Efficiency


class Global(models.Model):
    # Global Table
    sensex = models.FloatField(default=0)
    spread = models.IntegerField(default=0)
    LiveText = models.CharField(max_length=100)
    LeaderboardSize = models.IntegerField(default=100)
    LeaderBoardUpdateTime = models.DateTimeField(default=datetime.now)
    bidRangePercent = models.IntegerField(default=10, validators=[MaxValueValidator(100), MinValueValidator(1)])
    registrationKey = models.CharField(max_length=20, default="abcde")
    startStopMarket = models.BooleanField(default=True)  # True => start, False => Stop
    startNews = models.BooleanField(default=False)
    NewsCounter = models.IntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Extending User Model
    rank = models.IntegerField(default=-1)  # Rank of the user
    numberOfShares = models.IntegerField(default=0)  # Number of shares owned by the user
    cash = models.IntegerField(default=200000)  # Cash remaining
    netWorth = models.IntegerField(default=0)  # Users networth; Required for leaderboard;

    # Calculated using cash and number of shares

    def __str__(self):
        return self.user.username


class Company(models.Model):
    # Table to store all the company data
    name = models.CharField(max_length=25)  # Name of the company
    tempName = models.CharField(max_length=25)
    sharePrice = models.IntegerField(default=0)  # Company's share price
    totalNoOfShares = models.IntegerField(default=0)  # Total number of shares available for sale
    sharesLeft = models.IntegerField(default=0)  # Number of shares left  ########(Redundant?)ny.objects.all()

    def __str__(self):
        return self.name
