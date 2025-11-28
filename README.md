# ALX Travel App - Database Modeling and Data Seeding

Backend application for the ALX Travel platform built with Django and Django REST Framework.

## Features

### Database Models

The application includes three main models:

#### Listing Model
Represents a property listing available for booking.
- **Fields**: title, description, location, price_per_night, number_of_bedrooms, number_of_bathrooms, max_guests, available, host (ForeignKey to User)
- **Computed Property**: `average_rating` - calculates average rating from reviews
- **Relationships**: One-to-many with Booking and Review models

#### Booking Model
Represents a booking made by a guest for a listing.
- **Fields**: listing (ForeignKey), guest (ForeignKey to User), check_in, check_out, number_of_guests, total_price, status
- **Status Choices**: pending, confirmed, cancelled, completed
- **Computed Property**: `duration_nights` - calculates booking duration
- **Validation**: Ensures check-out is after check-in and guest count doesn't exceed listing capacity

#### Review Model
Represents a review left by a guest for a listing.
- **Fields**: listing (ForeignKey), guest (ForeignKey to User), rating (1-5), comment
- **Constraints**: Unique together on listing and guest (one review per guest per listing)
- **Validation**: Rating must be between 1 and 5

### API Serializers

Comprehensive serializers for data representation:
- `ListingSerializer` - Full listing data with nested host and reviews
- `BookingSerializer` - Booking data with nested listing and guest details
- `ReviewSerializer` - Review data with guest information
- `UserSerializer` - User profile data

All serializers include:
- Field validation
- Read-only computed fields
- Nested relationships
- Write-only ID fields for creating relationships

### Database Seeding

A management command to populate the database with sample data:

```bash
python manage.py seed
```

**Options:**
- `--clear` - Clear existing data before seeding

**Sample Data Created:**
- 4 users (2 hosts, 2 guests)
- 5 property listings in various locations
- 4 bookings with different statuses
- 4 reviews with ratings and comments

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL database
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jalloh19/alx_travel_app_0x00.git
cd alx_travel_app_0x00/alx_travel_app
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Seed the database:
```bash
python manage.py seed
```

7. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

8. Start the development server:
```bash
python manage.py runserver
```

## API Documentation

Swagger documentation is available at `/swagger/` once the development server is running.

## Project Structure

```
alx_travel_app/
├── alx_travel_app/
│   ├── listings/
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed.py          # Database seeding command
│   │   ├── models.py                # Database models
│   │   ├── serializers.py           # API serializers
│   │   ├── views.py                 # API views
│   │   └── urls.py                  # URL routing
│   ├── settings.py                  # Django settings
│   └── urls.py                      # Main URL configuration
├── manage.py
├── requirements.txt
└── README.md
```

## Technology Stack

- **Framework**: Django 4.2+
- **API**: Django REST Framework
- **Database**: MySQL
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Task Queue**: Celery
- **Message Broker**: RabbitMQ (configurable)

## Environment Variables

Key environment variables in `.env`:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=alx_travel_app_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306

CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Testing

Run tests with:
```bash
python manage.py test
```

## License

This project is part of the ALX Software Engineering program.
