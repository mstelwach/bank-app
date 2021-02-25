from django.urls import path

from transfer.views import *

app_name = 'transfer'

urlpatterns = [
    path('list/incoming/', IncomingTransferListView.as_view(), name='list-incoming'),
    path('list/outgoing/', OutgoingTransferListView.as_view(), name='list-outgoing'),
    path('detail/<pk>', TransferDetailView.as_view(), name='detail'),
    path('create/', TransferCreateView.as_view(), name='create')
]