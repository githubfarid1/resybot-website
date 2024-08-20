from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import os

class ReservationType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
            ordering = ["name"]

    def __str__(self) -> str:
        return self.name

class Proxy(models.Model):
    class Meta:
        ordering = ["name"]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    http = models.CharField(max_length=255, null=True, blank=True)
    https = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self) -> str:
        return self.name

class Account(models.Model):
    class Meta:
        ordering = ["email"]
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    api_key = models.CharField(max_length=255, null=True, blank=True)
    token =  models.CharField(max_length=1000, null=True, blank=True)
    payment_method_id = models.IntegerField(null=True, blank=True)
    def __str__(self) -> str:
        return self.email
    
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
    rundate = models.DateField()
    runtime = models.TimeField()
    runnow = models.BooleanField()
    nonstop = models.BooleanField()
    duration = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
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
    reservation = models.ForeignKey(
        ReservationType,
        db_column='reservation_id',
        on_delete=models.DO_NOTHING, 
        default=None
    )

class BotRun(models.Model):
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
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
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
    proxy_name = models.CharField(max_length=255, null=True, blank=True)
    proxy_http = models.CharField(max_length=255, null=True, blank=True)
    proxy_https = models.CharField(max_length=255, null=True, blank=True)
    reservation_name = models.CharField(max_length=255, null=True, blank=True)
    account_email = models.CharField(max_length=255, null=True, blank=True)
    account_password = models.CharField(max_length=255, null=True, blank=True)
    account_api_key = models.CharField(max_length=255, null=True, blank=True)
    account_token =  models.CharField(max_length=1000, null=True, blank=True)
    account_payment_method_id = models.IntegerField(null=True, blank=True)

    
# Create your models here.
