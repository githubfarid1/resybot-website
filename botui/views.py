from django.shortcuts import render
import os
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import ReservationType, Account, BotCommand, Proxy, BotRun, Multiproxy, BotCheck, BotCheckRun, Setting
import json
from .forms import ReservationForm, ProxyForm, AccountForm, BotCommandForm, MultiproxyForm, BotCheckForm, SettingForm
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.http import require_POST
from sys import platform
from subprocess import Popen, check_call, call, run, PIPE
import psutil
import linecache
import time
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.decorators import login_required

if platform == "linux" or platform == "linux2":
    pass
elif platform == "win32":
	from subprocess import CREATE_NEW_CONSOLE


PYLOC = settings.PYTHON_PATH
PIPLOC = settings.PIP_PATH

def run_module(comlist):
	if platform == "linux" or platform == "linux2":
		comlist[:0] = ["--"]
		comlist[:0] = ["gnome-terminal"]
		# print(comlist)
		Popen(comlist)
	elif platform == "win32":
		Popen(comlist, creationflags=CREATE_NEW_CONSOLE)
	
	comall = ''
	for com in comlist:
		comall += com + " "
	print(comall)

# Create your views here.

@login_required(login_url="login")
def show_reservations(request):
    context = {
    }
    return render(request=request, template_name='botui/show_reservations.html', context=context)

def reservation_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    reservations = ReservationType.objects.exclude(name='<Not Set>').all().order_by("name")
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

@login_required(login_url="login")
def show_accounts(request):
    context = {
    }
    return render(request=request, template_name='botui/show_accounts.html', context=context)

def account_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    accounts = Account.objects.exclude(email='<Not Set>').all()
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

def update_token(request, pk):
    account = get_object_or_404(Account, pk=pk)
    fname = open(f"logs/account_{account.id}.log", "w")
    process = Popen([PYLOC, "botmodules/update_token.py", "-em", account.email, "-pw", account.password], stdout=fname)
    # print(process.pid)
    # psutil.pid_exists(process.pid)
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "accountListChanged": None,
                "showMessage": f"{account.email} Updated."
            })
        })

def view_account_log(request, pk):
    account = get_object_or_404(Account, pk=pk)
    with open(f"logs/account_{pk}.log", 'r') as text_file:
        data = []
        for line in text_file:
            row = line.strip()
            # print(row)
            data.append(row)
    strlog = "\n".join(data)
    return render(request, 'botui/view_account_log.html', {
        'account': account,
        'module': 'View Log',
        "strlog": strlog
    })

def show_botcommands(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
    }
    return render(request=request, template_name='botui/show_botcommands.html', context=context)

def botcommand_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    botcommands = BotCommand.objects.all()
    return render(request, 'botui/botcommand_list.html', {
        'data': botcommands,
    })

def add_botcommand(request):
    if request.method == "POST":
        form = BotCommandForm(request.POST)
        if form.is_valid():
            botcommand = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "botcommandListChanged": None,
                        "showMessage": f"{botcommand.url} added."
                    })
                })
    else:
        form = BotCommandForm()
    return render(request, 'botui/botcommand_form.html', {
        'form': form,
        'module': 'Add Data'
    })

def edit_botcommand(request, pk):
    botcommand = get_object_or_404(BotCommand, pk=pk)
    # return HttpResponse(year.id)
    if request.method == "POST":
        form = BotCommandForm(request.POST, instance=botcommand)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "botcommandListChanged": None,
                        "showMessage": f"{botcommand.url} updated."
                    })
                }
            )
    else:
        form = BotCommandForm(instance=botcommand)
    return render(request, 'botui/botcommand_form.html', {
        'form': form,
        'botcommand': botcommand,
        'module': 'Edit Data'
    })

def remove_botcommand(request, pk):
    botcommand = get_object_or_404(BotCommand, pk=pk)
    botcommand.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "botcommandListChanged": None,
                "showMessage": f"{botcommand.url} deleted."
            })
        })

def run_botcommand(request, pk):
    botcommand = get_object_or_404(BotCommand, pk=pk)
    ret = BotRun.objects.create(url=botcommand.url, datewanted=botcommand.datewanted, timewanted=botcommand.timewanted, hoursba=botcommand.hoursba, seats=botcommand.seats, reservation_name=botcommand.reservation.name, rundate=botcommand.rundate, runtime=botcommand.runtime, runnow=botcommand.runnow, nonstop=botcommand.nonstop, duration=botcommand.duration, retry=botcommand.retry, minidle=botcommand.minidle, maxidle=botcommand.maxidle, account_email=botcommand.account.email, account_password=botcommand.account.password, account_api_key=botcommand.account.api_key, account_token=botcommand.account.token, account_payment_method_id=botcommand.account.payment_method_id, proxy_name=botcommand.proxy.name, proxy_http=botcommand.proxy.http, proxy_https=botcommand.proxy.https)
    # breakpoint()
    fname = open(f"logs/botrun_{ret.id}.log", "w")
    process = Popen([PYLOC, "botmodules/resybotv5b.py", "-id", '{}'.format(ret.id) ], stdout=fname)
    print(" ".join([PYLOC, "botmodules/resybotv5b.py", "-id", '{}'.format(ret.id) ]))
    BotRun.objects.filter(pk=ret.id).update(pid=process.pid)
    
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "botcommandListChanged": None,
                "showMessage": f"{botcommand.url} running."
            })
        })

def show_botruns(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
    }
    return render(request=request, template_name='botui/show_botruns.html', context=context)

def botrun_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    botruns = BotRun.objects.all()
    return render(request, 'botui/botrun_list.html', {
        'botruns': botruns,
    })

def remove_botrun(request, pk):
    # breakpoint()
    botrun = get_object_or_404(BotRun, pk=pk)
    try:
        os.remove(f"logs/botrun_{botrun.id}.log")
    except:
        pass
    try:
        proc = psutil.Process(int(botrun.pid))
        proc.terminate()
    except:
        pass
    botrun.delete()    
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "botrunListChanged": None,
                "showMessage": f"{botrun.url} deleted."
            })
        })

def tail(f, lines=20):
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = []
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            f.seek(0,0)
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count(b'\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = b''.join(reversed(blocks))
    return b'\n'.join(all_read_text.splitlines()[-total_lines_wanted:])

def view_botrun_log(request, pk):
    botrun = get_object_or_404(BotRun, pk=pk)
    strlog = ""
    with open(f"logs/botrun_{pk}.log", 'r') as file:
        strlog = file.read()
    # strlog = tail(file, 20)
    return render(request, 'botui/view_account_log.html', {
        'botrun': botrun,
        'module': 'View Log',
        "strlog": strlog
    })

@login_required(login_url="login")
def show_multiproxies(request):
    context = {
    }
    return render(request=request, template_name='botui/show_multiproxies.html', context=context)

def multiproxy_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    multiproxies = Multiproxy.objects.exclude(name='<Not Set>').all()
    return render(request, 'botui/multiproxy_list.html', {
        'data': multiproxies,
    })

def add_multiproxy(request):
    if request.method == "POST":
        form = MultiproxyForm(request.POST)
        if form.is_valid():
            multiproxy = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "proxyListChanged": None,
                        "showMessage": f"{multiproxy.name} added."
                    })
                })
    else:
        form = MultiproxyForm()
    return render(request, 'botui/multiproxy_form.html', {
        'form': form,
        'module': 'Add Data'
    })

def edit_multiproxy(request, pk):
    multiproxy = get_object_or_404(Multiproxy, pk=pk)
    # return HttpResponse(year.id)
    if request.method == "POST":
        form = MultiproxyForm(request.POST, instance=multiproxy)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "proxyListChanged": None,
                        "showMessage": f"{multiproxy.name} updated."
                    })
                }
            )
    else:
        form = MultiproxyForm(instance=multiproxy)
    return render(request, 'botui/multiproxy_form.html', {
        'form': form,
        'multiproxy': multiproxy,
        'module': 'Edit Data'
    })

def remove_multiproxy(request, pk):
    multiproxy = get_object_or_404(Multiproxy, pk=pk)
    multiproxy.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "proxyListChanged": None,
                "showMessage": f"{multiproxy.name} deleted."
            })
        })

@login_required(login_url="login")
def show_botchecks(request):
    context = {
    }
    return render(request=request, template_name='botui/show_botchecks.html', context=context)

@login_required(login_url="login")
def botcheck_list(request):
    botchecks = BotCheck.objects.all()
    return render(request, 'botui/botcheck_list.html', {
        'data': botchecks,
    })

@login_required(login_url="login")
def add_botcheck(request):
    if request.method == "POST":
        form = BotCheckForm(request.POST)
        if form.is_valid():
            botcheck = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "botcheckListChanged": None,
                        "showMessage": f"{botcheck.url} added."
                    })
                })
    else:
        form = BotCheckForm()
    return render(request, 'botui/botcheck_form.html', {
        'form': form,
        'module': 'Add Data'
    })

@login_required(login_url="login")
def edit_botcheck(request, pk):
    botcheck = get_object_or_404(BotCheck, pk=pk)
    # return HttpResponse(year.id)
    if request.method == "POST":
        form = BotCheckForm(request.POST, instance=botcheck)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "botcheckListChanged": None,
                        "showMessage": f"{botcheck.url} updated."
                    })
                }
            )
    else:
        form = BotCheckForm(instance=botcheck)
    return render(request, 'botui/botcheck_form.html', {
        'form': form,
        'botcheck': botcheck,
        'module': 'Edit Data'
    })

@login_required(login_url="login")
def remove_botcheck(request, pk):
    botcheck = get_object_or_404(BotCheck, pk=pk)
    botcheck.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "botcheckListChanged": None,
                "showMessage": f"{botcheck.url} deleted."
            })
        })

@login_required(login_url="login")
def run_botcheck(request, pk):
    botcheck = get_object_or_404(BotCheck, pk=pk)
    ret = BotCheckRun.objects.create(url=botcheck.url, startdate=botcheck.startdate, enddate=botcheck.enddate, seats=botcheck.seats, timewanted=botcheck.timewanted, hoursba=botcheck.hoursba, nonstop=botcheck.nonstop, reservation_name=botcheck.reservation.name, retrysec=botcheck.retrysec, minidle=botcheck.minidle, maxidle=botcheck.maxidle, account_email=botcheck.account.email, account_password=botcheck.account.password, account_api_key=botcheck.account.api_key, account_token=botcheck.account.token, account_payment_method_id=botcheck.account.payment_method_id, multiproxy_name=botcheck.multiproxy.name, multiproxy_value=botcheck.multiproxy.value, task=1, sendmessage=botcheck.sendmessage, username=request.user.username, mentionto=botcheck.mentionto, minproxy=botcheck.minproxy, maxproxy=botcheck.maxproxy)
    # fname = open(f"logs/checkbookrun_web_{ret.id}.log", "w")
    # commandlist = [PYLOC, "botmodules/resybotcheckbooking.py", "-id", '{}'.format(ret.id) ]
    # process = Popen(commandlist, stdout=fname)
    # print(" ".join(commandlist))
    # BotCheckRun.objects.filter(pk=ret.id).update(pid=process.pid)
    # print(process.pid)
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "botcheckListChanged": None,
                "showMessage": f"{botcheck.url} running."
            })
        })

@login_required(login_url="login")
def show_botcheckruns(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
    }
    return render(request=request, template_name='botui/show_botcheckruns.html', context=context)

@login_required(login_url="login")
def botcheckrun_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    botcheckruns = BotCheckRun.objects.filter(~Q(task=3)).all()
    for idx, bot in enumerate(botcheckruns):
        stat = "Stopped"
        bgcolor = "bg-success"
            
        # if bot.pid != 0 and psutil.pid_exists(bot.pid):
        #     if psutil.Process(bot.pid).status() != 'zombie':
        #         stat = "Running"
        #         bgcolor="bg-danger"
        if bot.task == 1 and bot.pid != -1:
            stat = "Running"
            bgcolor="bg-danger"

        botcheckruns[idx].pidstatus = stat
        botcheckruns[idx].bgcolor = bgcolor

    return render(request, 'botui/botcheckrun_list.html', {
        'botcheckruns': botcheckruns,
    })

@login_required(login_url="login")
def remove_botcheckrun(request, pk):
    botcheckrun = get_object_or_404(BotCheckRun, pk=pk)
    botcheckrun.task = 3
    botcheckrun.save()

    # pid = botcheckrun.pid
    
    # try:
    #     proc = psutil.Process(int(pid))
    #     proc.terminate()
    # except:
    #     pass

    # botcheckrun.delete()
    # time.sleep(0.5)        
    # try:
    #     os.remove(f"logs/checkbookrun_web_{pk}.log")
    # except:
    #     pass

    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "botcheckrunListChanged": None,
                "showMessage": f"{botcheckrun.url} deleted."
            })
        })

@login_required(login_url="login")
def view_checkbookrun_log(request, pk):
    botrun = get_object_or_404(BotCheckRun, pk=pk)
    strlog = ""
    if platform == "linux" or platform == "linux2":
        result = run(["tail", "-1000", f"logs/checkbookrun_web_{pk}.log"], stdout=PIPE)
        strlog = result.stdout.decode('utf-8')
    return render(request, 'botui/view_checkbookrun_log.html', {
        'botrun': botrun,
        'module': 'View Log',
        "strlog": strlog
    })

@login_required(login_url="login")
def download_checkbookrun_log(request, pk):
    # botrun = get_object_or_404(BotCheckRun, pk=pk)
    filename = f"checkbookrun_web_{pk}.log"
    read_file = open(f"logs/{filename}", "r")
    response = HttpResponse(read_file.read(), content_type="text/plain,charset=utf8")
    read_file.close()
       
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    return response



@login_required(login_url="login")
def stop_botcheckrun(request, pk):
    # breakpoint()
    botcheckrun = get_object_or_404(BotCheckRun, pk=pk)
    # pid = botcheckrun.pid
    # try:
    #     proc = psutil.Process(int(pid))
    #     proc.terminate()
    # except:
    #     pass
    botcheckrun.task = 2
    botcheckrun.save()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "botcheckrunListChanged": None,
                "showMessage": f"{botcheckrun.url} stopped."
            })
        })

@login_required(login_url="login")
def show_settings(request):
    context = {
    }
    return render(request=request, template_name='botui/show_settings.html', context=context)

@login_required(login_url="login")
def setting_list(request):
    settings = Setting.objects.all()
    return render(request, 'botui/setting_list.html', {
        'data': settings,
    })

@login_required(login_url="login")
def edit_setting(request, pk):
    setting = get_object_or_404(Setting, pk=pk)
    # return HttpResponse(year.id)
    if request.method == "POST":
        form = SettingForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "settingListChanged": None,
                        "showMessage": f"{setting.name} updated."
                    })
                }
            )
    else:
        form = SettingForm(instance=setting)
    return render(request, 'botui/setting_form.html', {
        'form': form,
        'setting': setting,
        'module': 'Edit Data'
    })

@login_required(login_url="login")
def add_setting(request):
    if request.method == "POST":
        form = SettingForm(request.POST)
        if form.is_valid():
            setting = form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "settingListChanged": None,
                        "showMessage": f"{setting.key} added."
                    })
                })
    else:
        form = SettingForm()
    return render(request, 'botui/setting_form.html', {
        'form': form,
        'module': 'Add Data'
    })
