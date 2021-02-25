from django.urls import path

from card.views import *

app_name = 'card'

urlpatterns = [
    path('list/', CardListView.as_view(), name='list'),
    path('detail/<pk>', CardDetailView.as_view(), name='detail'),
    path('create/', CardCreateView.as_view(), name='create')
]