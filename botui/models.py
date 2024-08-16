from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import os

class ReservationType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Proxy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    http = models.CharField(max_length=255)
    https = models.CharField(max_length=255)

class Account(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255, null=True, blank=True)
    token =  models.CharField(max_length=1000, null=True, blank=True)
    payment_method_id = models.IntegerField(null=True, blank=True)

class BotCommand(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()
    datewanted = models.DateField()
    timewanted = models.TimeField()
    hoursba = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(12)]
    )
    seats = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )
    reservation = models.CharField(max_length=255)
    rundate = models.DateField()
    runtime = models.TimeField()
    runnow = models.BooleanField()
    nonstop = models.BooleanField()
    duration = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )
    retry = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)]
    )
    minidle = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(600)]
    )
    maxidle = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(600)]
    )
    account = models.ForeignKey(
        Account,
        db_column='account_id',
        on_delete=models.DO_NOTHING, 
        default=None
    )
    proxy = models.ForeignKey(
        Proxy,
        db_column='proxy_id',
        on_delete=models.DO_NOTHING, 
        default=None
    )

    def __str__(self) -> str:
        return str(self.yeardate)


     
# Create your models here.
