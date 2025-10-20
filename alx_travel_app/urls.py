from django.urls import path, include

urlpatterns = [
    path('api/', include('alx_travel_app.listings.urls')),
]
