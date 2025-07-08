from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from .models import Trade
from .serializers import TradeSerializer, TradeListSerializer


class TradeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing trades.
    
    Provides CRUD operations for trades:
    - GET /api/trades/ - List all trades
    - POST /api/trades/ - Create a new trade
    - GET /api/trades/{id}/ - Retrieve a specific trade
    - PUT /api/trades/{id}/ - Update a trade
    - PATCH /api/trades/{id}/ - Partially update a trade
    - DELETE /api/trades/{id}/ - Delete a trade
    """
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    
    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.action == 'list':
            return TradeListSerializer
        return TradeSerializer
    
    def get_queryset(self):
        """Filter queryset based on query parameters."""
        queryset = Trade.objects.all()
        
        # Filter by symbol
        symbol = self.request.query_params.get('symbol', None)
        if symbol:
            queryset = queryset.filter(symbol__iexact=symbol.upper())
        
        # Filter by trade type
        trade_type = self.request.query_params.get('trade_type', None)
        if trade_type:
            queryset = queryset.filter(trade_type=trade_type.upper())
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(trade_date__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(trade_date__date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get portfolio summary statistics.
        GET /api/trades/summary/
        """
        trades = self.get_queryset()
        
        # Calculate summary statistics
        total_trades = trades.count()
        total_buy_value = trades.filter(trade_type='BUY').aggregate(
            total=Sum('total_value')
        )['total'] or 0
        total_sell_value = trades.filter(trade_type='SELL').aggregate(
            total=Sum('total_value')
        )['total'] or 0
        
        # Get unique symbols
        symbols = trades.values_list('symbol', flat=True).distinct()
        
        # Calculate symbol-wise statistics
        symbol_stats = []
        for symbol in symbols:
            symbol_trades = trades.filter(symbol=symbol)
            buy_quantity = symbol_trades.filter(trade_type='BUY').aggregate(
                total=Sum('quantity')
            )['total'] or 0
            sell_quantity = symbol_trades.filter(trade_type='SELL').aggregate(
                total=Sum('quantity')
            )['total'] or 0
            net_quantity = buy_quantity - sell_quantity
            
            symbol_stats.append({
                'symbol': symbol,
                'buy_quantity': buy_quantity,
                'sell_quantity': sell_quantity,
                'net_quantity': net_quantity,
                'total_buy_value': float(symbol_trades.filter(trade_type='BUY').aggregate(
                    total=Sum('total_value')
                )['total'] or 0),
                'total_sell_value': float(symbol_trades.filter(trade_type='SELL').aggregate(
                    total=Sum('total_value')
                )['total'] or 0),
            })
        
        return Response({
            'total_trades': total_trades,
            'total_buy_value': float(total_buy_value),
            'total_sell_value': float(total_sell_value),
            'net_value': float(total_buy_value - total_sell_value),
            'symbols': list(symbols),
            'symbol_stats': symbol_stats,
        })
    
    @action(detail=False, methods=['get'])
    def symbols(self, request):
        """
        Get list of all unique symbols.
        GET /api/trades/symbols/
        """
        symbols = Trade.objects.values_list('symbol', flat=True).distinct().order_by('symbol')
        return Response({'symbols': list(symbols)}) 