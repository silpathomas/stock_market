from rest_framework import serializers
from .models import StockUser


class StockUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockUser
        fields = ('user', 'account_balance','earnt','spent','created_at', 'updated_at')

    def update(self, instance, validated_data):

        #adding balance to current wallet amount
        current_balance=StockUser.objects.get(pk=instance.pk).account_balance
        instance.account_balance = validated_data.get('account_balance', instance.account_balance)+current_balance

        instance.save()
        return instance