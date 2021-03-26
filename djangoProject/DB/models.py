from datetime import datetime
from django.db import models


class Courier(models.Model):
    courier_id = models.IntegerField(primary_key=True)
    courier_type = models.CharField(max_length=5)
    regions = models.CharField(max_length=200)
    working_hours = models.CharField(max_length=200)
    assign_time = models.DateTimeField(default=datetime.now())  # дефолт - 0, может хранить datetimr
    last_time = models.DateTimeField(default=datetime.now())
    orders = models.CharField(max_length=200, default="[]")
    last_assign_courier_type = models.CharField(max_length=5)
    earnings = models.IntegerField(default=0)


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    weight = models.FloatField()
    region = models.IntegerField()
    delivery_hours = models.CharField(max_length=200)  # взят ли заказ
    taken = models.BooleanField(default=False)


class Value_coruier(models.Model):
    courier_id = models.IntegerField()
    region = models.IntegerField()
    sum_time = models.FloatField(default=0)
    counts = models.IntegerField(default=0)
