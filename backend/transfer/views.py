from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from account.models import BankAccount
from transfer.forms import TransferCreateForm
from transfer.models import Transfer


class TransferCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Transfer
    form_class = TransferCreateForm
    template_name = 'transfer/create.html'
    success_url = reverse_lazy('index')
    success_message = "Your transfer was created successfully."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get(self, request, *args, **kwargs):
        if request.is_ajax and request.GET.get('sender'):
            sender = BankAccount.objects.get(pk=request.GET.get('sender'))
            return JsonResponse({'sender_max_amount': sender.current_balance})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.status = 'CT'
        sender = form.cleaned_data.get('sender')
        receiver = form.cleaned_data.get('receiver')
        amount = form.cleaned_data.get('amount')

        # Update current balance sender and receiver
        sender.current_balance -= amount
        receiver.current_balance += amount
        sender.save()
        receiver.save()
        return super().form_valid(form)


class IncomingTransferListView(LoginRequiredMixin, ListView):
    model = Transfer
    template_name = 'transfer/incoming_list.html'

    def get_queryset(self):
        return Transfer.objects.filter(receiver__in=self.request.user.bank_accounts.all())


class OutgoingTransferListView(LoginRequiredMixin, ListView):
    model = Transfer
    template_name = 'transfer/outgoing_list.html'

    def get_queryset(self):
        return Transfer.objects.filter(sender__in=self.request.user.bank_accounts.all())


class TransferDetailView(LoginRequiredMixin, DetailView):
    model = Transfer
    template_name = 'transfer/detail.html'
