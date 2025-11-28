"""Management command to seed the database with sample data."""

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from alx_travel_app.listings.models import Booking, Listing, Review


class Command(BaseCommand):
    """Django management command to populate database with sample listings."""

    help = "Seeds the database with sample listings, bookings, and reviews"

    def add_arguments(self, parser):
        """Add optional arguments for the command."""
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        """Execute the seed command."""
        if options["clear"]:
            self.stdout.write("Clearing existing data...")
            Booking.objects.all().delete()
            Review.objects.all().delete()
            Listing.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS("✓ Data cleared"))

        self.stdout.write("Seeding database...")

        # Create sample users
        users = self._create_users()
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(users)} users"))

        # Create sample listings
        listings = self._create_listings(users)
        self.stdout.write(
            self.style.SUCCESS(f"✓ Created {len(listings)} listings")
        )

        # Create sample bookings
        bookings = self._create_bookings(listings, users)
        self.stdout.write(
            self.style.SUCCESS(f"✓ Created {len(bookings)} bookings")
        )

        # Create sample reviews
        reviews = self._create_reviews(listings, users)
        self.stdout.write(
            self.style.SUCCESS(f"✓ Created {len(reviews)} reviews")
        )

        self.stdout.write(
            self.style.SUCCESS(
                "\n✓ Database seeded successfully with sample data!"
            )
        )

    def _create_users(self):
        """Create sample users."""
        users_data = [
            {
                "username": "john_host",
                "email": "john@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "password123",
            },
            {
                "username": "jane_host",
                "email": "jane@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "password": "password123",
            },
            {
                "username": "bob_guest",
                "email": "bob@example.com",
                "first_name": "Bob",
                "last_name": "Johnson",
                "password": "password123",
            },
            {
                "username": "alice_guest",
                "email": "alice@example.com",
                "first_name": "Alice",
                "last_name": "Williams",
                "password": "password123",
            },
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults={
                    "email": user_data["email"],
                    "first_name": user_data["first_name"],
                    "last_name": user_data["last_name"],
                },
            )
            if created:
                user.set_password(user_data["password"])
                user.save()
            users.append(user)

        return users

    def _create_listings(self, users):
        """Create sample listings."""
        listings_data = [
            {
                "title": "Cozy Downtown Apartment",
                "description": "A beautiful apartment in the heart of the city with modern amenities and stunning views.",
                "location": "New York, NY",
                "price_per_night": Decimal("150.00"),
                "number_of_bedrooms": 2,
                "number_of_bathrooms": 1,
                "max_guests": 4,
                "available": True,
                "host": users[0],
            },
            {
                "title": "Beachfront Villa",
                "description": "Luxurious villa right on the beach with private pool and direct ocean access.",
                "location": "Miami, FL",
                "price_per_night": Decimal("350.00"),
                "number_of_bedrooms": 4,
                "number_of_bathrooms": 3,
                "max_guests": 8,
                "available": True,
                "host": users[0],
            },
            {
                "title": "Mountain Cabin Retreat",
                "description": "Peaceful cabin surrounded by nature, perfect for a quiet getaway.",
                "location": "Aspen, CO",
                "price_per_night": Decimal("200.00"),
                "number_of_bedrooms": 3,
                "number_of_bathrooms": 2,
                "max_guests": 6,
                "available": True,
                "host": users[1],
            },
            {
                "title": "Urban Loft Studio",
                "description": "Modern loft in trendy neighborhood with easy access to restaurants and shops.",
                "location": "San Francisco, CA",
                "price_per_night": Decimal("120.00"),
                "number_of_bedrooms": 1,
                "number_of_bathrooms": 1,
                "max_guests": 2,
                "available": True,
                "host": users[1],
            },
            {
                "title": "Historic Townhouse",
                "description": "Charming townhouse with classic architecture and modern updates.",
                "location": "Boston, MA",
                "price_per_night": Decimal("180.00"),
                "number_of_bedrooms": 3,
                "number_of_bathrooms": 2,
                "max_guests": 5,
                "available": False,
                "host": users[0],
            },
        ]

        listings = []
        for listing_data in listings_data:
            listing, _ = Listing.objects.get_or_create(
                title=listing_data["title"], defaults=listing_data
            )
            listings.append(listing)

        return listings

    def _create_bookings(self, listings, users):
        """Create sample bookings."""
        today = date.today()

        bookings_data = [
            {
                "listing": listings[0],
                "guest": users[2],
                "check_in": today + timedelta(days=7),
                "check_out": today + timedelta(days=10),
                "number_of_guests": 2,
                "total_price": Decimal("450.00"),
                "status": "confirmed",
            },
            {
                "listing": listings[1],
                "guest": users[3],
                "check_in": today + timedelta(days=14),
                "check_out": today + timedelta(days=21),
                "number_of_guests": 4,
                "total_price": Decimal("2450.00"),
                "status": "pending",
            },
            {
                "listing": listings[2],
                "guest": users[2],
                "check_in": today - timedelta(days=10),
                "check_out": today - timedelta(days=5),
                "number_of_guests": 3,
                "total_price": Decimal("1000.00"),
                "status": "completed",
            },
            {
                "listing": listings[3],
                "guest": users[3],
                "check_in": today + timedelta(days=3),
                "check_out": today + timedelta(days=5),
                "number_of_guests": 1,
                "total_price": Decimal("240.00"),
                "status": "confirmed",
            },
        ]

        bookings = []
        for booking_data in bookings_data:
            booking, _ = Booking.objects.get_or_create(
                listing=booking_data["listing"],
                guest=booking_data["guest"],
                check_in=booking_data["check_in"],
                defaults=booking_data,
            )
            bookings.append(booking)

        return bookings

    def _create_reviews(self, listings, users):
        """Create sample reviews."""
        reviews_data = [
            {
                "listing": listings[0],
                "guest": users[2],
                "rating": 5,
                "comment": "Amazing place! Very clean and exactly as described. Great location.",
            },
            {
                "listing": listings[1],
                "guest": users[3],
                "rating": 4,
                "comment": "Beautiful villa with stunning ocean views. A bit pricey but worth it.",
            },
            {
                "listing": listings[2],
                "guest": users[2],
                "rating": 5,
                "comment": "Perfect mountain getaway. So peaceful and relaxing. Highly recommend!",
            },
            {
                "listing": listings[0],
                "guest": users[3],
                "rating": 4,
                "comment": "Great apartment in a convenient location. Would stay again.",
            },
        ]

        reviews = []
        for review_data in reviews_data:
            review, _ = Review.objects.get_or_create(
                listing=review_data["listing"],
                guest=review_data["guest"],
                defaults=review_data,
            )
            reviews.append(review)

        return reviews
