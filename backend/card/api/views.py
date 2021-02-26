from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from card.api.filters import CardFilter
from card.api.serializers import CardSerializer
from card.models import Card


class CardViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = CardFilter

    # def get_queryset(self):
    #     return Card.objects.filter(account__user=self.request.user)


