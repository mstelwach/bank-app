from django.urls import path

from account.views import *

app_name = 'account'

user_urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='create'),
    path('detail/<pk>/', UserDetailView.as_view(), name='detail'),
    path('password/change/', UserPasswordChangeView.as_view(), name='password-change'),
    path('password/reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('password/reset/done/', UserPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password/reset/confirm/<uidb64>/<token>/',
         UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password/reset/complete/', UserPasswordResetCompleteView.as_view(), name='password-reset-complete'),
]

bank_account_urlpatterns = [
    path('bank-account/list/', BankAccountListView.as_view(), name='bank-account-list'),
    path('bank-account/detail/<pk>/', BankAccountDetailView.as_view(), name='bank-account-detail'),
    path('bank-account/create/', BankAccountCreateView.as_view(), name='bank-account-create')

]
urlpatterns = user_urlpatterns + bank_account_urlpatterns
