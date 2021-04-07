from django.urls import path

from . import views

urlpatterns = [
    path('buy_alicoins', views.buy_alicoins, name='buy_alicoins'),
    path('import_key', views.import_key, name='import_key'),
    path('ipfs_test', views.ipfs_test, name='ipfs_test'),
]