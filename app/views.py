from django.shortcuts import render
from intasend import APIService
from django.conf import settings
from django.http import JsonResponse
import requests


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

        url = "https://sandbox.intasend.com/api/v1/payment/mpesa-stk-push/"

        payload = {
            "amount": amount,
            "phone_number": phone_number
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {settings.INTASEND_API_TOKEN}"
        }

        response = requests.post(url, json=payload, headers=headers)
        print('Response', response.status_code)
        if response.status_code == 200:
            response_details = response.json()
            invoice_id = response_details.get('invoice', {}).get('invoice_id')
            print('Invoice Id', invoice_id)
            # print('Response data', response_details)
            success_message = "STK push sent successfully. Please check your phone to complete the payment."
            return render(request, 'initiate_payment.html', {'success': success_message})
        else:
            error_message = f"Failed to send STK push. Status:"
            return render(request, 'initiate_payment.html', {'error': error_message})
    return render(request, 'initiate_payment.html')



def check_payment_status(request):
    url = "https://sandbox.intasend.com/api/v1/payment/status/"

    payload = { "invoice_id": "YVO9VZQ" }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer ISSecretKey_test_96dd8981-fa1f-4ccd-841e-8aa9932ebebe"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
