#!/usr/bin/env python3
"""
Test script to demonstrate the Portfolio Tracker API functionality.
Run this after starting the Django server.
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000/api"

def test_api():
    """Test the API endpoints with sample data."""
    
    print("🚀 Testing Portfolio Tracker API")
    print("=" * 50)
    
    # Test 1: Create some sample trades
    print("\n1. Creating sample trades...")
    
    sample_trades = [
        {
            "symbol": "AAPL",
            "trade_type": "BUY",
            "quantity": 10,
            "price": 150.50,
            "notes": "Initial Apple position"
        },
        {
            "symbol": "GOOGL",
            "trade_type": "BUY",
            "quantity": 5,
            "price": 2800.00,
            "notes": "Google stock purchase"
        },
        {
            "symbol": "AAPL",
            "trade_type": "SELL",
            "quantity": 3,
            "price": 160.00,
            "notes": "Partial profit taking"
        },
        {
            "symbol": "MSFT",
            "trade_type": "BUY",
            "quantity": 8,
            "price": 300.00,
            "notes": "Microsoft position"
        }
    ]
    
    created_trades = []
    for trade in sample_trades:
        response = requests.post(f"{BASE_URL}/trades/", json=trade)
        if response.status_code == 201:
            created_trade = response.json()
            created_trades.append(created_trade)
            print(f"✅ Created trade: {created_trade['symbol']} {created_trade['trade_type']} {created_trade['quantity']} @ ${created_trade['price']}")
        else:
            print(f"❌ Failed to create trade: {response.text}")
    
    # Test 2: List all trades
    print("\n2. Listing all trades...")
    response = requests.get(f"{BASE_URL}/trades/")
    if response.status_code == 200:
        trades = response.json()
        print(f"✅ Found {trades['count']} trades")
        for trade in trades['results']:
            print(f"   - {trade['symbol']} {trade['trade_type']} {trade['quantity']} @ ${trade['price']} (Total: {trade['formatted_total_value']})")
    else:
        print(f"❌ Failed to list trades: {response.text}")
    
    # Test 3: Get portfolio summary
    print("\n3. Getting portfolio summary...")
    response = requests.get(f"{BASE_URL}/trades/summary/")
    if response.status_code == 200:
        summary = response.json()
        print(f"✅ Portfolio Summary:")
        print(f"   - Total trades: {summary['total_trades']}")
        print(f"   - Total buy value: ${summary['total_buy_value']:,.2f}")
        print(f"   - Total sell value: ${summary['total_sell_value']:,.2f}")
        print(f"   - Net value: ${summary['net_value']:,.2f}")
        print(f"   - Symbols: {', '.join(summary['symbols'])}")
        
        print(f"\n   Symbol Statistics:")
        for stat in summary['symbol_stats']:
            print(f"   - {stat['symbol']}: Net {stat['net_quantity']} shares (Buy: {stat['buy_quantity']}, Sell: {stat['sell_quantity']})")
    else:
        print(f"❌ Failed to get summary: {response.text}")
    
    # Test 4: Filter trades by symbol
    print("\n4. Filtering trades by symbol (AAPL)...")
    response = requests.get(f"{BASE_URL}/trades/?symbol=AAPL")
    if response.status_code == 200:
        trades = response.json()
        print(f"✅ Found {trades['count']} AAPL trades")
        for trade in trades['results']:
            print(f"   - {trade['trade_type']} {trade['quantity']} @ ${trade['price']}")
    else:
        print(f"❌ Failed to filter trades: {response.text}")
    
    # Test 5: Get all symbols
    print("\n5. Getting all symbols...")
    response = requests.get(f"{BASE_URL}/trades/symbols/")
    if response.status_code == 200:
        symbols = response.json()
        print(f"✅ Symbols: {', '.join(symbols['symbols'])}")
    else:
        print(f"❌ Failed to get symbols: {response.text}")
    
    # Test 6: Update a trade
    if created_trades:
        print("\n6. Updating a trade...")
        trade_id = created_trades[0]['id']
        update_data = {
            "notes": "Updated note - This trade was modified"
        }
        response = requests.patch(f"{BASE_URL}/trades/{trade_id}/", json=update_data)
        if response.status_code == 200:
            updated_trade = response.json()
            print(f"✅ Updated trade {trade_id}: {updated_trade['notes']}")
        else:
            print(f"❌ Failed to update trade: {response.text}")
    
    # Test 7: Get specific trade
    if created_trades:
        print("\n7. Getting specific trade...")
        trade_id = created_trades[0]['id']
        response = requests.get(f"{BASE_URL}/trades/{trade_id}/")
        if response.status_code == 200:
            trade = response.json()
            print(f"✅ Trade {trade_id}: {trade['symbol']} {trade['trade_type']} {trade['quantity']} @ ${trade['price']}")
        else:
            print(f"❌ Failed to get trade: {response.text}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print(f"📊 Access the admin interface at: http://localhost:8000/admin/")
    print(f"🔗 API root at: {BASE_URL}/")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the Django server is running:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}") 