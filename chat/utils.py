from trading.models import *
buy_keywords = [
    "buy",
    "purchase",
    "bid",
    "obtain",
    "get",
    "take",
    "bought",
    "buying",
    "purchasing",
    "bidding",
    "getting",
    "taking",
    "obtaining",
    "khareed",
    "khareedna",
    "lena",
    "le",
]

sell_keywords = ["sell", "selling", "sold", "dena", "bechna", "bech,de"]

company_name=[company.name.lower() for company in Company.objects.all()]