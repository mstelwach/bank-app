from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from card.forms import CardCreateForm
from card.models import Card


class CardCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Card
    form_class = CardCreateForm
    template_name = 'card/create.html'
    success_url = reverse_lazy('index')
    success_message = "Your card was created successfully."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = 'card/list.html'


class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = 'card/detail.html'
