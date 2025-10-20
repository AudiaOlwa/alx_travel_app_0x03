import requests
from django.http import JsonResponse
from django.conf import settings
from .models import Payment
import uuid

def initiate_payment(request):
    if request.method == "POST":
        data = request.POST
        booking_ref = data.get("booking_reference")
        amount = data.get("amount")
        email = data.get("email")

        tx_ref = str(uuid.uuid4())

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "amount": amount,
            "currency": "ETB",
            "email": email,
            "tx_ref": tx_ref,
            "callback_url": settings.CHAPA_CALLBACK_URL,
            "return_url": "http://127.0.0.1:8000/success/",
            "customization": {"title": "Travel Booking Payment"}
        }

        response = requests.post("https://api.chapa.co/v1/transaction/initialize", 
                                 json=payload, headers=headers)

        res_data = response.json()

        if response.status_code == 200 and res_data.get("status") == "success":
            Payment.objects.create(
                booking_reference=booking_ref,
                amount=amount,
                transaction_id=tx_ref,
                status="pending"
            )
            return JsonResponse({
                "checkout_url": res_data["data"]["checkout_url"],
                "transaction_id": tx_ref
            })
        else:
            return JsonResponse({"error": "Payment initialization failed", "details": res_data}, status=400)


def verify_payment(request):
    tx_ref = request.GET.get("tx_ref")

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
    }

    response = requests.get(f"https://api.chapa.co/v1/transaction/verify/{tx_ref}", headers=headers)
    res_data = response.json()

    try:
        payment = Payment.objects.get(transaction_id=tx_ref)
    except Payment.DoesNotExist:
        return JsonResponse({"error": "Payment not found"}, status=404)

    if res_data.get("status") == "success":
        payment.status = "completed"
        payment.save()
        return JsonResponse({"message": "Payment successful", "data": res_data})
    else:
        payment.status = "failed"
        payment.save()
        return JsonResponse({"message": "Payment failed", "data": res_data}, status=400)
