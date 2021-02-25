from rest_framework.serializers import ModelSerializer

from transfer.models import Transfer


class TransferSerializer(ModelSerializer):

    class Meta:
        model = Transfer
        fields = ('sender', 'receiver', 'title', 'amount', 'currency', 'reference', 'status', 'method', )
        extra_kwargs = {
            'created': {
                'required': False
            }
        }