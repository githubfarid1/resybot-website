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
    
]