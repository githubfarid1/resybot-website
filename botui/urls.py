from django.urls import path
from botui import views
# print(__package__)
prefix = __package__ + "_"
urlpatterns = [
    path(route='reservations', view=views.show_reservations, name=prefix + "show_reservations"),
    path(route='reservation_list', view=views.reservation_list, name=prefix + "reservation_list"),
    path(route='add_reservation', view=views.add_reservation, name=prefix + "add_reservation"),
    path(route='reservation/<int:pk>/edit', view=views.edit_reservation, name=prefix + "edit_reservation"),
    path(route='reservation/<int:pk>/remove', view=views.remove_reservation, name=prefix + 'remove_reservation'),

    path(route='proxies', view=views.show_proxies, name=prefix + "show_proxies"),
    path(route='proxy_list', view=views.proxy_list, name=prefix + "proxy_list"),
    path(route='add_proxy', view=views.add_proxy, name=prefix + "add_proxy"),
    path(route='proxy/<int:pk>/edit', view=views.edit_proxy, name=prefix + "edit_proxy"),
    path(route='proxy/<int:pk>/remove', view=views.remove_proxy, name=prefix + 'remove_proxy'),

    path(route='accounts', view=views.show_accounts, name=prefix + "show_accounts"),
    path(route='account_list', view=views.account_list, name=prefix + "account_list"),
    path(route='add_account', view=views.add_account, name=prefix + "add_account"),
    path(route='account/<int:pk>/edit', view=views.edit_account, name=prefix + "edit_account"),
    path(route='account/<int:pk>/remove', view=views.remove_account, name=prefix + 'remove_account'),
    path(route='account/<int:pk>/update_token', view=views.update_token, name=prefix + 'update_token'),
    path(route='account/<int:pk>/view_account_log', view=views.view_account_log, name=prefix + 'view_account_log'),
    
    path(route='botcommands', view=views.show_botcommands, name=prefix + "show_botcommands"),
    path(route='botcommand_list', view=views.botcommand_list, name=prefix + "botcommand_list"),
    path(route='add_botcommand', view=views.add_botcommand, name=prefix + "add_botcommand"),
    path(route='botcommand/<int:pk>/edit', view=views.edit_botcommand, name=prefix + "edit_botcommand"),
    path(route='botcommand/<int:pk>/remove', view=views.remove_botcommand, name=prefix + 'remove_botcommand'),
    path(route='botcommand/<int:pk>/run', view=views.run_botcommand, name=prefix + 'run_botcommand'),
 
    path(route='botruns', view=views.show_botruns, name=prefix + "show_botruns"),
    path(route='botrun_list', view=views.botrun_list, name=prefix + "botrun_list"),
    path(route='botrun/<int:pk>/remove', view=views.remove_botrun, name=prefix + 'remove_botrun'),
    path(route='botrun/<int:pk>/view_botrun_log', view=views.view_botrun_log, name=prefix + 'view_botrun_log'),
 
    path(route='multiproxies', view=views.show_multiproxies, name=prefix + "show_multiproxies"),
    path(route='multiproxy_list', view=views.multiproxy_list, name=prefix + "multiproxy_list"),
    path(route='add_multiproxy', view=views.add_multiproxy, name=prefix + "add_multiproxy"),
    path(route='multiproxy/<int:pk>/edit', view=views.edit_multiproxy, name=prefix + "edit_multiproxy"),
    path(route='multiproxy/<int:pk>/remove', view=views.remove_multiproxy, name=prefix + 'remove_multiproxy'),

   path(route='botchecks', view=views.show_botchecks, name=prefix + "show_botchecks"),
    path(route='botcheck_list', view=views.botcheck_list, name=prefix + "botcheck_list"),
    path(route='add_botcheck', view=views.add_botcheck, name=prefix + "add_botcheck"),
    path(route='botcheck/<int:pk>/edit', view=views.edit_botcheck, name=prefix + "edit_botcheck"),
    path(route='botcheck/<int:pk>/remove', view=views.remove_botcheck, name=prefix + 'remove_botcheck'),
    path(route='botcheck/<int:pk>/run', view=views.run_botcheck, name=prefix + 'run_botcheck'),
 
    path(route='botcheckruns', view=views.show_botcheckruns, name=prefix + "show_botcheckruns"),
    path(route='botcheckrun_list', view=views.botcheckrun_list, name=prefix + "botcheckrun_list"),
    path(route='botcheckrun/<int:pk>/remove', view=views.remove_botcheckrun, name=prefix + 'remove_botcheckrun'),
    path(route='botcheckrun/<int:pk>/view_checkbookrun_log', view=views.view_checkbookrun_log, name=prefix + 'view_checkbookrun_log'),
   path(route='botcheckrun/<int:pk>/stop', view=views.stop_botcheckrun, name=prefix + 'stop_botcheckrun'),
 
]