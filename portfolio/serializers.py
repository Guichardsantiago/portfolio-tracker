from rest_framework import serializers
from .models import Trade


class TradeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Trade model.
    """
    formatted_total_value = serializers.ReadOnlyField()
    formatted_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Trade
        fields = [
            'id', 'symbol', 'trade_type', 'quantity', 'price', 
            'trade_date', 'notes', 'total_value', 
            'formatted_total_value', 'formatted_price'
        ]
        read_only_fields = ['id', 'trade_date', 'total_value']
    
    def validate(self, data):
        """
        Custom validation for trade data.
        """
        # Ensure symbol is uppercase
        if 'symbol' in data:
            data['symbol'] = data['symbol'].upper()
        
        # Validate price is positive
        if 'price' in data and data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        
        # Validate quantity is positive
        if 'quantity' in data and data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        
        return data


class TradeListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing trades.
    """
    formatted_total_value = serializers.ReadOnlyField()
    formatted_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Trade
        fields = [
            'id', 'symbol', 'trade_type', 'quantity', 'price', 
            'trade_date', 'total_value', 'formatted_total_value', 'formatted_price'
        ] 