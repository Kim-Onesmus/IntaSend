from django.shortcuts import render
from intasend import APIService
from django.conf import settings
from django.http import JsonResponse


def get_intasend_service():
    return APIService(
        token=settings.INTASEND_API_TOKEN,
        publishable_key=settings.INTASEND_PUBLISHABLE_KEY,
        test=settings.INTASEND_TEST_MODE
    )


def initiate_payment(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        service = get_intasend_service()
        response = service.collect.mpesa_stk_push(
            phone_number=phone_number,
            email=email,
            amount=amount,
            narrative="Payment for Services"
        )

        return JsonResponse(response)
    return render(request, 'initiate_payment.html')

# views.py

def check_payment_status(request, invoice_id):
    service = get_intasend_service()
    status_response = service.collect.status(invoice_id=invoice_id)
    return JsonResponse(status_response)
