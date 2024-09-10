from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from datetime import datetime, date
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
    pid = models.IntegerField(null=True, blank=True)
    
class Multiproxy(models.Model):
    class Meta:
        ordering = ["name"]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    value = models.TextField(null=True, blank=True)
    def __str__(self) -> str:
        return self.name


class BotCheck(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()
    startdate = models.DateField()
    enddate = models.DateField()
    seats = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )

    timewanted = models.TimeField()
    hoursba = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(12)]
    )
    nonstop = models.BooleanField()
    minidle = models.DecimalField(max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0.5), MaxValueValidator(600)]
    )
    maxidle = models.DecimalField(max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0.5), MaxValueValidator(600)]
    )
    retrysec = models.DecimalField(max_digits=3, decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(9.99)]
    )
    sendmessage = models.BooleanField(default=False)
    account = models.ForeignKey(
        Account,
        db_column='account_id',
        on_delete=models.DO_NOTHING, 
        default=None
    )
    multiproxy = models.ForeignKey(
        Multiproxy,
        db_column='multiproxy_id',
        on_delete=models.DO_NOTHING, 
        default=None
    )
    reservation = models.ForeignKey(
        ReservationType,
        db_column='reservation_id',
        on_delete=models.DO_NOTHING, 
        default=None
    )


class BotCheckRun(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()
    startdate = models.DateField()
    enddate = models.DateField()
    seats = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000)]
    )

    timewanted = models.TimeField()
    hoursba = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(12)]
    )
    nonstop = models.BooleanField()
    minidle = models.DecimalField(max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0.5), MaxValueValidator(600)]
    )
    maxidle = models.DecimalField(max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0.5), MaxValueValidator(600)]
    )
    retrysec = models.DecimalField(max_digits=3, decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(9.99)]
    )
    sendmessage = models.BooleanField(default=False)
    multiproxy_name = models.CharField(max_length=255, null=True, blank=True)
    multiproxy_value = models.CharField(max_length=255, null=True, blank=True)
    reservation_name = models.CharField(max_length=255, null=True, blank=True)
    account_email = models.CharField(max_length=255, null=True, blank=True)
    account_password = models.CharField(max_length=255, null=True, blank=True)
    account_api_key = models.CharField(max_length=255, null=True, blank=True)
    account_token =  models.CharField(max_length=1000, null=True, blank=True)
    account_payment_method_id = models.IntegerField(null=True, blank=True)
    pid = models.IntegerField(null=True, blank=True, default=0)
    task = models.IntegerField(default=0)
    '''
    1=run
    2=stop
    3=delete
    
    '''
# Create your models here.
