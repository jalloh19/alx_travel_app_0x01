"""Database models for the listings application."""

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Listing(models.Model):
    """Represents a property listing available for booking."""

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_bedrooms = models.PositiveIntegerField()
    number_of_bathrooms = models.PositiveIntegerField()
    max_guests = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings",
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["location"]),
            models.Index(fields=["price_per_night"]),
            models.Index(fields=["available"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.location}"

    @property
    def average_rating(self):
        """Calculate the average rating from all reviews."""
        reviews = self.reviews.all()
        if reviews.exists():
            return reviews.aggregate(models.Avg("rating"))["rating__avg"]
        return None


class Booking(models.Model):
    """Represents a booking made by a guest for a listing."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    guest = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["check_in", "check_out"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Booking #{self.id} - {self.listing.title} by {self.guest.username}"

    def clean(self):
        """Validate booking data."""
        from django.core.exceptions import ValidationError

        if self.check_out <= self.check_in:
            raise ValidationError("Check-out date must be after check-in date.")

        if self.number_of_guests > self.listing.max_guests:
            raise ValidationError(
                f"Number of guests exceeds listing capacity ({self.listing.max_guests})."
            )

    @property
    def duration_nights(self):
        """Calculate the number of nights for this booking."""
        return (self.check_out - self.check_in).days


class Review(models.Model):
    """Represents a review left by a guest for a listing."""

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    guest = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["listing", "guest"]
        indexes = [
            models.Index(fields=["rating"]),
        ]

    def __str__(self):
        return f"Review by {self.guest.username} for {self.listing.title} - {self.rating}/5"


class Payment(models.Model):
    """Represents a payment for a booking."""
    
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"
