#!/usr/bin/env python3
"""Serializers for the listings app."""

from rest_framework import serializers
from .models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model."""
    host = serializers.CharField(source="host.username", read_only=True)

    class Meta:
        model = Listing
        fields = ("id", "title", "description", "price", "host", "created_at")
        read_only_fields = ("id", "host", "created_at")


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model."""
    user = serializers.CharField(source="user.username", read_only=True)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())

    class Meta:
        model = Booking
        fields = (
            "id",
            "listing",
            "user",
            "start_date",
            "end_date",
            "total_price",
            "created_at",
        )
        read_only_fields = ("id", "user", "created_at")
