# Portfolio Tracker API

A Django REST API for tracking portfolio trades with comprehensive CRUD operations.

## Features

- **Trade Management**: Create, read, update, and delete trades
- **Portfolio Analytics**: Get summary statistics and symbol-wise breakdowns
- **Filtering**: Filter trades by symbol, trade type, and date range
- **Automatic Calculations**: Total value is calculated automatically
- **Admin Interface**: Full Django admin integration for data management

## Tech Stack

- **Django 4.2.7**: Web framework
- **Django REST Framework 3.14.0**: API framework
- **SQLite**: Database (can be easily changed to PostgreSQL, MySQL, etc.)
- **CORS Headers**: Cross-origin resource sharing support

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Trade Management

#### List All Trades
```
GET /api/trades/
```

**Query Parameters:**
- `symbol`: Filter by stock symbol (e.g., `?symbol=AAPL`)
- `trade_type`: Filter by trade type (`BUY` or `SELL`)
- `start_date`: Filter trades from this date (YYYY-MM-DD)
- `end_date`: Filter trades until this date (YYYY-MM-DD)

**Example:**
```bash
curl http://localhost:8000/api/trades/?symbol=AAPL&trade_type=BUY
```

#### Create a New Trade
```
POST /api/trades/
```

**Request Body:**
```json
{
    "symbol": "AAPL",
    "trade_type": "BUY",
    "quantity": 10,
    "price": 150.50,
    "notes": "Bought Apple stock"
}
```

#### Get Specific Trade
```
GET /api/trades/{id}/
```

#### Update Trade
```
PUT /api/trades/{id}/
PATCH /api/trades/{id}/
```

#### Delete Trade
```
DELETE /api/trades/{id}/
```

### Portfolio Analytics

#### Get Portfolio Summary
```
GET /api/trades/summary/
```

**Response:**
```json
{
    "total_trades": 25,
    "total_buy_value": 15000.00,
    "total_sell_value": 5000.00,
    "net_value": 10000.00,
    "symbols": ["AAPL", "GOOGL", "MSFT"],
    "symbol_stats": [
        {
            "symbol": "AAPL",
            "buy_quantity": 100,
            "sell_quantity": 20,
            "net_quantity": 80,
            "total_buy_value": 15000.00,
            "total_sell_value": 3000.00
        }
    ]
}
```

#### Get All Symbols
```
GET /api/trades/symbols/
```

**Response:**
```json
{
    "symbols": ["AAPL", "GOOGL", "MSFT", "TSLA"]
}
```

## Trade Model Fields

| Field | Type | Description | Required |
|-------|------|-------------|----------|
| `symbol` | CharField | Stock symbol (e.g., AAPL) | Yes |
| `trade_type` | CharField | BUY or SELL | Yes |
| `quantity` | PositiveIntegerField | Number of shares | Yes |
| `price` | DecimalField | Price per share | Yes |
| `trade_date` | DateTimeField | Trade timestamp | Auto |
| `notes` | TextField | Additional notes | No |
| `total_value` | DecimalField | Calculated total | Auto |

## Example Usage

### Create a Buy Trade
```bash
curl -X POST http://localhost:8000/api/trades/ \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "trade_type": "BUY",
    "quantity": 10,
    "price": 150.50,
    "notes": "Bought Apple stock"
  }'
```

### Create a Sell Trade
```bash
curl -X POST http://localhost:8000/api/trades/ \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "trade_type": "SELL",
    "quantity": 5,
    "price": 160.00,
    "notes": "Sold half position"
  }'
```

### Get Portfolio Summary
```bash
curl http://localhost:8000/api/trades/summary/
```

### Filter Trades by Symbol
```bash
curl http://localhost:8000/api/trades/?symbol=AAPL
```

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to manage trades through a web interface.

## Development

### Running Tests
```bash
python manage.py test
```

### Making Changes
1. Modify models in `portfolio/models.py`
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`

## Production Deployment

For production deployment:

1. Change `DEBUG = False` in `settings.py`
2. Set a proper `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Use a production database (PostgreSQL recommended)
5. Set up proper CORS settings
6. Use a production WSGI server (Gunicorn, uWSGI)

## License

This project is open source and available under the MIT License.