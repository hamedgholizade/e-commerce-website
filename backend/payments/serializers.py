from rest_framework import serializers

from payments.models import Payment


class PeymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields = [
            'id',
            'order',
            'status',
            'transaction_id',
            'amount',
            'reference_id',
            'card_pan',
            'fee',
            'payment_date',
            'updated_at',
            'created_at',
            'is_active'
        ]
        read_only_fields = [
            'id',
            'order',
            'status',
            'transaction_id',
            'amount',
            'reference_id',
            'card_pan',
            'fee',
            'payment_date',
            'updated_at',
            'created_at',
            'is_active'
        ]
