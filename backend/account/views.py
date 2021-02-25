import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from account.forms import UserPasswordResetForm, LoginForm, BankAccountCreateForm, UserCreateForm
from account.models import User, BankAccount
from transfer.models import Transfer


class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    datetime = timezone.now()

    def get_last_month_data(self, today):
        '''
        Simple method to get the datetime objects for the
        start and end of last month.
        '''
        this_month_start = datetime.datetime(today.year, today.month, 1)
        last_month_end = this_month_start - datetime.timedelta(days=1)
        last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
        return last_month_start, last_month_end

    def get_month_data_range(self, months_ago=1, include_this_month=False):
        '''
        A method that generates a list of dictionaires
        that describe any given amout of monthly data.
        '''
        today = datetime.datetime.now().today()
        dates_ = []
        if include_this_month:
            # get next month's data with:
            next_month = today.replace(day=28) + datetime.timedelta(days=4)
            # use next month's data to get this month's data breakdown
            start, end = self.get_last_month_data(next_month)
            dates_.insert(0, {
                "start": start,
                "end": end,
            })
        for x in range(0, months_ago):
            start, end = self.get_last_month_data(today)
            today = start
            dates_.insert(0, {
                "start": start,
                "end": end,
            })
        return dates_

    def get_range_amount_transfers(self, months_ago, include_this_month, transfers_type):
        range_stats = self.get_month_data_range(months_ago, include_this_month)
        amounts = []
        for month in range_stats:
            transfers = []
            if transfers_type == 'incoming':
                transfers = Transfer.objects.filter(receiver__user=self.request.user,
                                                    created__date__gte=month['start'],
                                                    created__date__lte=month['end'])

            if transfers_type == 'outgoing':
                transfers = Transfer.objects.filter(sender__user=self.request.user,
                                                    created__date__gte=month['start'],
                                                    created__date__lte=month['end'])

            total_amounts_month = sum(transfers.values_list('amount', flat=True))
            amounts.append(total_amounts_month)

        return amounts

    def get_daily_amounts_transfers(self):
        # GET DAILY QUERYSET IN AND OUT TRANSFERS
        incoming_transfers = Transfer.objects.filter(receiver__user=self.request.user,
                                                     created__date=self.datetime.date())
        outgoing_transfers = Transfer.objects.filter(sender__user=self.request.user,
                                                     created__date=self.datetime.date())

        # GET EARNINGS AND EXPENSES
        earnings = sum(incoming_transfers.values_list('amount', flat=True))
        expenses = sum(outgoing_transfers.values_list('amount', flat=True))

        transfers = {
            'earnings': earnings,
            'expenses': expenses
        }

        return transfers

    def get_current_month_transfers_count(self):
        today = datetime.datetime.now().today()
        next_month = today.replace(day=28) + datetime.timedelta(days=4)
        start, end = self.get_last_month_data(next_month)
        incoming_transfers = Transfer.objects.filter(receiver__user=self.request.user,
                                                     created__date__gte=start,
                                                     created__date__lte=end)
        outgoing_transfers = Transfer.objects.filter(sender__user=self.request.user,
                                                     created__date__gte=start,
                                                     created__date__lte=end)
        transfers_count = {
            'incoming': len(incoming_transfers),
            'outgoing': len(outgoing_transfers)
        }
        return transfers_count

    def get_context_data(self, **kwargs):
        kwargs = super(HomePage, self).get_context_data(**kwargs)

        daily_transfers = self.get_daily_amounts_transfers()
        monthly_incoming_transfers = self.get_range_amount_transfers(0, True, 'incoming')
        monthly_outgoing_transfers = self.get_range_amount_transfers(0, True, 'outgoing')

        kwargs.update({
            'earnings': {
                'daily': daily_transfers['earnings'],
                'monthly': sum(monthly_incoming_transfers),
            },
            'expenses': {
                'daily': daily_transfers['expenses'],
                'monthly': sum(monthly_outgoing_transfers)
            }
        })

        return kwargs

    def post(self, request, *args, **kwargs):
        if request.is_ajax:
            incoming_data = [int(amount) for amount in self.get_range_amount_transfers(11, True, 'incoming')]
            outgoing_data = [int(amount) for amount in self.get_range_amount_transfers(11, True, 'outgoing')]

            monthly_transfers_count = self.get_current_month_transfers_count()

            return JsonResponse({
                'incoming_data': incoming_data,
                'outgoing_data': outgoing_data,
                'incoming_count': monthly_transfers_count['incoming'],
                'outgoing_count': monthly_transfers_count['outgoing']
            })


class Login(LoginView):
    template_name = 'account/login.html'
    form_class = LoginForm


class Logout(LoginRequiredMixin, LogoutView):
    pass


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'account/create.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('account:login')
    success_message = "Your account was created successfully."


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'account/detail.html'
    queryset = User.objects.all()


class UserPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = "account/password_change.html"
    success_url = reverse_lazy('account:detail')
    success_message = "The passwords was changed successfully."


class UserPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset_form.html'
    form_class = UserPasswordResetForm
    success_url = reverse_lazy('account:password-reset-confirm')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'
    success_url = reverse_lazy('account:password-reset-complete')


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password-reset-complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class BankAccountCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = BankAccount
    form_class = BankAccountCreateForm
    template_name = 'account/bank_account/create.html'
    success_url = reverse_lazy('index')
    success_message = "Your account bank was created successfully."

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BankAccountListView(LoginRequiredMixin, ListView):
    model = BankAccount
    template_name = 'account/bank_account/list.html'

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)


class BankAccountDetailView(LoginRequiredMixin, DetailView):
    model = BankAccount
    template_name = 'account/bank_account/detail.html'
