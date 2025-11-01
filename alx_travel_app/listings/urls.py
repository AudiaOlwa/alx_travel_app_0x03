from django.urls import path, include
from rest_framework.routers import DefaultRouter
from alx_travel_app.listings.views import ListingViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]