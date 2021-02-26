from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from transfer.api.filters import TransferFilter
from transfer.api.serializers import TransferSerializer
from transfer.models import Transfer


class TransferViewSet(ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = TransferFilter

    # def get_queryset(self):
    #     return Transfer.objects.filter(sender__user=self.request.user, receiver__user=self.request.user)


