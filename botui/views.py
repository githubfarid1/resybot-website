from django.shortcuts import render
import os
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import ReservationType, Account, BotCommand, Proxy
import json
from .forms import ReservationForm, ProxyForm, AccountForm
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.

def show_reservations(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
    }
    return render(request=request, template_name='botui/show_reservations.html', context=context)

def reservation_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    reservations = ReservationType.objects.all()
    return render(request, 'botui/reservation_list.html', {
        'data': reservations,
    })

def add_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "reservationListChanged": None,
                        "showMessage": f"{reservation.name} added."
                    })
                })
    else:
        form = ReservationForm()
    return render(request, 'botui/reservation_form.html', {
        'form': form,
        'module': 'Add Data'
    })

def edit_reservation(request, pk):
    reservation = get_object_or_404(ReservationType, pk=pk)
    # return HttpResponse(year.id)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "reservationListChanged": None,
                        "showMessage": f"{reservation.name} updated."
                    })
                }
            )
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'botui/reservation_form.html', {
        'form': form,
        'reservation': reservation,
        'module': 'Edit Data'
    })

def remove_reservation(request, pk):
    reservation = get_object_or_404(ReservationType, pk=pk)
    reservation.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "reservationListChanged": None,
                "showMessage": f"{reservation.name} deleted."
            })
        })


def show_proxies(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
    }
    return render(request=request, template_name='botui/show_proxies.html', context=context)

def proxy_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    proxies = Proxy.objects.all()
    return render(request, 'botui/proxy_list.html', {
        'data': proxies,
    })

def add_proxy(request):
    if request.method == "POST":
        form = ProxyForm(request.POST)
        if form.is_valid():
            proxy = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "proxyListChanged": None,
                        "showMessage": f"{proxy.name} added."
                    })
                })
    else:
        form = ProxyForm()
    return render(request, 'botui/proxy_form.html', {
        'form': form,
        'module': 'Add Data'
    })

def edit_proxy(request, pk):
    proxy = get_object_or_404(Proxy, pk=pk)
    # return HttpResponse(year.id)
    if request.method == "POST":
        form = ProxyForm(request.POST, instance=proxy)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "proxyListChanged": None,
                        "showMessage": f"{proxy.name} updated."
                    })
                }
            )
    else:
        form = ProxyForm(instance=proxy)
    return render(request, 'botui/proxy_form.html', {
        'form': form,
        'proxy': proxy,
        'module': 'Edit Data'
    })

def remove_proxy(request, pk):
    proxy = get_object_or_404(Proxy, pk=pk)
    proxy.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "proxyListChanged": None,
                "showMessage": f"{proxy.name} deleted."
            })
        })


def show_accounts(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
    }
    return render(request=request, template_name='botui/show_accounts.html', context=context)

def account_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    accounts = Account.objects.all()
    return render(request, 'botui/account_list.html', {
        'data': accounts,
    })

def add_account(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "accountListChanged": None,
                        "showMessage": f"{account.email} added."
                    })
                })
    else:
        form = AccountForm()
    return render(request, 'botui/account_form.html', {
        'form': form,
        'module': 'Add Data'
    })

def edit_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    # return HttpResponse(year.id)
    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "accountListChanged": None,
                        "showMessage": f"{account.email} updated."
                    })
                }
            )
    else:
        form = AccountForm(instance=account)
    return render(request, 'botui/account_form.html', {
        'form': form,
        'account': account,
        'module': 'Edit Data'
    })

def remove_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    account.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "accountListChanged": None,
                "showMessage": f"{account.email} deleted."
            })
        })
