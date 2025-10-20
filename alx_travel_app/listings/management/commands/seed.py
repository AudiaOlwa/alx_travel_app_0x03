#!/usr/bin/env python3
"""Management command to seed the DB with sample listings."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing
from decimal import Decimal


class Command(BaseCommand):
    """Seed listings into the database."""

    help = "Create sample users and listings for local development."

    def handle(self, *args, **options):
        User = get_user_model()
        host, created = User.objects.get_or_create(
            username="seeder",
            defaults={"email": "seeder@example.com", "is_active": True},
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Created host user 'seeder'."))

        sample_listings = [
            {
                "title": "Cozy studio in city center",
                "description": "Small but well-located studio with all amenities.",
                "price": Decimal("45.00"),
            },
            {
                "title": "Spacious countryside cottage",
                "description": "Peaceful cottage surrounded by nature.",
                "price": Decimal("120.00"),
            },
            {
                "title": "Modern apartment near transit",
                "description": "Great view, fast Wi-Fi, close to transport.",
                "price": Decimal("75.50"),
            },
        ]

        created_count = 0
        for item in sample_listings:
            listing, _ = Listing.objects.get_or_create(
                title=item["title"],
                defaults={
                    "description": item["description"],
                    "price": item["price"],
                    "host": host,
                },
            )
            if _:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} listings."))
