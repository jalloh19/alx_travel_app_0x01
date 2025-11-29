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

### API Endpoints

All API endpoints are accessible under `/api/` following RESTful conventions.

#### Listing Endpoints

- **List all listings**: `GET /api/listings/`
- **Create a listing**: `POST /api/listings/`
- **Retrieve a listing**: `GET /api/listings/{id}/`
- **Update a listing**: `PUT /api/listings/{id}/`
- **Partial update**: `PATCH /api/listings/{id}/`
- **Delete a listing**: `DELETE /api/listings/{id}/`

**Query Parameters** (for listing):
- `location` - Filter by location (case-insensitive)
- `available` - Filter by availability (true/false)
- `min_price` - Filter by minimum price per night
- `max_price` - Filter by maximum price per night

#### Booking Endpoints

- **List all bookings**: `GET /api/bookings/`
- **Create a booking**: `POST /api/bookings/`
- **Retrieve a booking**: `GET /api/bookings/{id}/`
- **Update a booking**: `PUT /api/bookings/{id}/`
- **Partial update**: `PATCH /api/bookings/{id}/`
- **Delete a booking**: `DELETE /api/bookings/{id}/`

**Query Parameters** (for bookings):
- `status` - Filter by booking status (pending, confirmed, cancelled, completed)
- `guest_id` - Filter by guest user ID
- `listing_id` - Filter by listing ID

### Testing with Postman

#### 1. GET - List All Listings
```
GET http://localhost:8000/api/listings/
```

#### 2. GET - List Listings with Filters
```
GET http://localhost:8000/api/listings/?location=paris&available=true&min_price=50&max_price=200
```

#### 3. POST - Create a New Listing
```
POST http://localhost:8000/api/listings/
Content-Type: application/json

{
  "title": "Cozy Apartment in Downtown",
  "description": "Beautiful apartment with city views",
  "location": "New York",
  "price_per_night": "150.00",
  "number_of_bedrooms": 2,
  "number_of_bathrooms": 1,
  "max_guests": 4,
  "available": true,
  "host_id": 1
}
```

#### 4. GET - Retrieve a Specific Listing
```
GET http://localhost:8000/api/listings/1/
```

#### 5. PUT - Update a Listing
```
PUT http://localhost:8000/api/listings/1/
Content-Type: application/json

{
  "title": "Updated Cozy Apartment",
  "description": "Newly renovated apartment with city views",
  "location": "New York",
  "price_per_night": "175.00",
  "number_of_bedrooms": 2,
  "number_of_bathrooms": 1,
  "max_guests": 4,
  "available": true,
  "host_id": 1
}
```

#### 6. PATCH - Partial Update a Listing
```
PATCH http://localhost:8000/api/listings/1/
Content-Type: application/json

{
  "price_per_night": "180.00",
  "available": false
}
```

#### 7. DELETE - Delete a Listing
```
DELETE http://localhost:8000/api/listings/1/
```

#### 8. POST - Create a New Booking
```
POST http://localhost:8000/api/bookings/
Content-Type: application/json

{
  "listing_id": 1,
  "guest_id": 2,
  "check_in": "2025-12-15",
  "check_out": "2025-12-20",
  "number_of_guests": 2,
  "total_price": "750.00",
  "status": "pending"
}
```

#### 9. GET - List Bookings with Filters
```
GET http://localhost:8000/api/bookings/?status=confirmed&guest_id=2
```

#### 10. PUT - Update a Booking Status
```
PUT http://localhost:8000/api/bookings/1/
Content-Type: application/json

{
  "listing_id": 1,
  "guest_id": 2,
  "check_in": "2025-12-15",
  "check_out": "2025-12-20",
  "number_of_guests": 2,
  "total_price": "750.00",
  "status": "confirmed"
}
```

### Testing with cURL

#### List All Listings
```bash
curl -X GET http://localhost:8000/api/listings/
```

#### Create a Listing
```bash
curl -X POST http://localhost:8000/api/listings/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beach House",
    "description": "Stunning beachfront property",
    "location": "Miami",
    "price_per_night": "250.00",
    "number_of_bedrooms": 3,
    "number_of_bathrooms": 2,
    "max_guests": 6,
    "available": true,
    "host_id": 1
  }'
```

#### Get a Specific Listing
```bash
curl -X GET http://localhost:8000/api/listings/1/
```

#### Update a Listing
```bash
curl -X PATCH http://localhost:8000/api/listings/1/ \
  -H "Content-Type: application/json" \
  -d '{"available": false}'
```

#### Delete a Listing
```bash
curl -X DELETE http://localhost:8000/api/listings/1/
```

#### Create a Booking
```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "listing_id": 1,
    "guest_id": 2,
    "check_in": "2025-12-15",
    "check_out": "2025-12-20",
    "number_of_guests": 2,
    "total_price": "750.00",
    "status": "pending"
  }'
```

#### List Bookings with Filter
```bash
curl -X GET "http://localhost:8000/api/bookings/?status=confirmed"
```

### Expected Response Formats

#### Listing Response
```json
{
  "id": 1,
  "title": "Cozy Apartment in Downtown",
  "description": "Beautiful apartment with city views",
  "location": "New York",
  "price_per_night": "150.00",
  "number_of_bedrooms": 2,
  "number_of_bathrooms": 1,
  "max_guests": 4,
  "available": true,
  "host": {
    "id": 1,
    "username": "host1",
    "email": "host1@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "average_rating": 4.5,
  "reviews": [],
  "created_at": "2025-11-29T10:00:00Z",
  "updated_at": "2025-11-29T10:00:00Z"
}
```

#### Booking Response
```json
{
  "id": 1,
  "listing": {
    "id": 1,
    "title": "Cozy Apartment in Downtown",
    "location": "New York"
  },
  "guest": {
    "id": 2,
    "username": "guest1",
    "email": "guest1@example.com"
  },
  "check_in": "2025-12-15",
  "check_out": "2025-12-20",
  "number_of_guests": 2,
  "total_price": "750.00",
  "status": "pending",
  "duration_nights": 5,
  "created_at": "2025-11-29T10:00:00Z",
  "updated_at": "2025-11-29T10:00:00Z"
}
```

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
