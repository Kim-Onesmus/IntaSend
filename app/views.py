from django.shortcuts import render, redirect
from intasend import APIService
from django.conf import settings
from django.http import JsonResponse
import requests
import time
import json


def get_intasend_service():
    return APIService(
        token=settings.INTASEND_API_TOKEN,
        publishable_key=settings.INTASEND_PUBLISHABLE_KEY,
        test=settings.INTASEND_TEST_MODE
    )



def initiate_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        phone_number = data.get('phone_number')
        amount = data.get('amount')
        email = data.get('email')


        url = f"{settings.BASE_URL}/api/v1/payment/mpesa-stk-push/"

        payload = {
            "amount": amount,
            "phone_number": phone_number,
            "email":email
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {settings.INTASEND_API_TOKEN}"
        }

        response = requests.post(url, json=payload, headers=headers)
        print('Response', response.text)
        if response.status_code == 200:
            response_details = response.json()
            invoice_id = response_details.get('invoice', {}).get('invoice_id')
            print('Invoice Id', invoice_id)
            return JsonResponse({
                'status':200,
                'invoice_id': invoice_id,
            })
        else:
            return JsonResponse({
                'status':500,
            })
    return render(request, 'initiate_payment.html')



def check_payment_status(request):
    url = f"{settings.BASE_URL}/api/v1/payment/status/"
    invoice_id = request.GET.get('invoice_id')
    print('Invoice Id', invoice_id)
    if not invoice_id:
        return JsonResponse({
            'status': 400,
            'message': 'Invoice ID is required'
        })
    payload = { 
        "invoice_id": invoice_id 
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {settings.INTASEND_API_TOKEN}"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        state = response_data.get('invoice', {}).get('state')
        if state != "COMPLETE":
            return JsonResponse({
                'status': 202,
                'message': 'Validating payment, please wait'
            })
        elif state == 'COMPLETE':
            return JsonResponse({
                'status': 200,
                'message': 'Payment successful, redirecting....'
            })
        else:
            return JsonResponse({
                'status': 201,
                'message': 'An error occured while validatin payment'
            })
