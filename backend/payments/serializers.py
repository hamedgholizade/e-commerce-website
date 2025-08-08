from rest_framework import serializers

from payments.models import Payment


class PeymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = '__all__'
