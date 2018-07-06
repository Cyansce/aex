from django.db import models
from django.utils import timezone

import datetime
# Create your models here.

class Zone(models.Model):
    name = models.CharField(max_length=50)
    create_at = models.DateTimeField('创建时间', default=timezone.now)

    def __str__(self):
        return self.name


    

class Coin(models.Model):
    name = models.CharField(max_length=50)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 



class APIAccount(models.Model):
    name = models.CharField(max_length = 50)
    key = models.CharField(max_length = 200)
    skey = models.CharField(max_length = 200)
    user_id = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Account(models.Model):
    is_api = models.BooleanField()
    name = models.CharField(max_length = 50, null=True)

    url = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    md5 = models.CharField(max_length = 200, null=True)
    user_id = models.CharField(max_length=20, null=True)
    update_md5_at = models.DateTimeField(null=True)

    key = models.CharField(max_length = 200, null=True)
    skey = models.CharField(max_length = 200, null=True)
    
    def __str__(self):
        return self.name



class OrderLog(models.Model):
    is_api = models.BooleanField()
    account_id = models.IntegerField()
    account_name = models.CharField(max_length=50)

    is_strategy = models.BooleanField(False) # 是否为策略单 
    is_strategy_complete = models.BooleanField(default=False) # 是否为策略单且完成
    is_cancel = models.BooleanField(default=False) # 是否撤单
    complete = models.BooleanField(False)
    coin_name = models.CharField(max_length=20)
    zone_name = models.CharField(max_length=20)
    trade_type = models.IntegerField()
    number = models.CharField(max_length=20, null=True)
    price = models.FloatField(null=True)
    amount = models.FloatField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)


class StrategyOrderLoop(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    # is_api = models.BooleanField()
    # account_id = models.IntegerField()
    zone_name = models.CharField(max_length=20)
    coin_name = models.CharField(max_length=20)
    percent = models.FloatField()
    point = models.IntegerField()

    start_time = models.DateTimeField(null=True)
    max_price = models.FloatField(null=True)
    min_price = models.FloatField(null=True)

class OrderLoopNumbersLog(models.Model):
    number = models.CharField(max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)

class ReservationOrder(models.Model):
    number = models.CharField(max_length=20)
    trade_type = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    reservation_price = models.FloatField()
    coin_name = models.CharField(max_length=20) # 币种
    zone_name = models.CharField(max_length=20) # 交易区
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)

    is_complete = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)

class APIConfig(models.Model):
    url = models.CharField(max_length=200)
    

