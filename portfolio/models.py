from django.db import models
from django.core.validators import MinValueValidator


class Trade(models.Model):
    """
    Model to represent a trade in the portfolio.
    """
    TRADE_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    
    symbol = models.CharField(max_length=10, help_text="Stock symbol (e.g., AAPL, GOOGL)")
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES, help_text="Buy or Sell")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], help_text="Number of shares")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], help_text="Price per share")
    trade_date = models.DateTimeField(auto_now_add=True, help_text="Date and time of the trade")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the trade")
    
    # Calculated fields
    total_value = models.DecimalField(max_digits=12, decimal_places=2, help_text="Total value of the trade (quantity * price)")
    
    class Meta:
        ordering = ['-trade_date']
        verbose_name = "Trade"
        verbose_name_plural = "Trades"
    
    def save(self, *args, **kwargs):
        """Override save to calculate total_value automatically."""
        self.total_value = self.quantity * self.price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.trade_type} {self.quantity} {self.symbol} @ ${self.price}"
    
    @property
    def formatted_total_value(self):
        """Return formatted total value."""
        return f"${self.total_value:,.2f}"
    
    @property
    def formatted_price(self):
        """Return formatted price."""
        return f"${self.price:,.2f}" 