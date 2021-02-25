from django_filters.rest_framework import FilterSet

from transfer.models import Transfer


class TransferFilter(FilterSet):
    class Meta:
        model = Transfer
        fields = ('method', 'status', )

