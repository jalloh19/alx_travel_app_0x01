"""Serializers for API data representation."""

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Booking, Listing, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id"]


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""

    guest = UserSerializer(read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="guest",
        write_only=True,
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "listing",
            "guest",
            "guest_id",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_rating(self, value):
        """Ensure rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model."""

    host = UserSerializer(read_only=True)
    host_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="host",
        write_only=True,
    )
    average_rating = serializers.ReadOnlyField()
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "description",
            "location",
            "price_per_night",
            "number_of_bedrooms",
            "number_of_bathrooms",
            "max_guests",
            "available",
            "host",
            "host_id",
            "average_rating",
            "reviews",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_price_per_night(self, value):
        """Ensure price is positive."""
        if value <= 0:
            raise serializers.ValidationError(
                "Price per night must be greater than zero."
            )
        return value

    def validate(self, data):
        """Validate listing data."""
        if data.get("number_of_bedrooms", 0) < 0:
            raise serializers.ValidationError(
                "Number of bedrooms cannot be negative."
            )
        if data.get("number_of_bathrooms", 0) < 0:
            raise serializers.ValidationError(
                "Number of bathrooms cannot be negative."
            )
        if data.get("max_guests", 0) <= 0:
            raise serializers.ValidationError(
                "Maximum guests must be at least 1."
            )
        return data


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model."""

    listing = ListingSerializer(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(),
        source="listing",
        write_only=True,
    )
    guest = UserSerializer(read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="guest",
        write_only=True,
    )
    duration_nights = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "listing",
            "listing_id",
            "guest",
            "guest_id",
            "check_in",
            "check_out",
            "number_of_guests",
            "total_price",
            "status",
            "duration_nights",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, data):
        """Validate booking data."""
        check_in = data.get("check_in")
        check_out = data.get("check_out")
        listing = data.get("listing")
        number_of_guests = data.get("number_of_guests")

        if check_out <= check_in:
            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )

        if listing and number_of_guests > listing.max_guests:
            raise serializers.ValidationError(
                f"Number of guests exceeds listing capacity ({listing.max_guests})."
            )

        if number_of_guests <= 0:
            raise serializers.ValidationError(
                "Number of guests must be at least 1."
            )

        return data

    def validate_total_price(self, value):
        """Ensure total price is positive."""
        if value <= 0:
            raise serializers.ValidationError(
                "Total price must be greater than zero."
            )
        return value
