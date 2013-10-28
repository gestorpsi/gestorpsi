#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template.context import RequestContext

from packages.paypal.standard.forms import PayPalPaymentsForm
from gestorpsi import settings


def single_payment(request):
    paypal_dict = {
        "currency_code": "BRL",
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        
        "amount": 1000,
        "item_name": "Testes de integração",
        'item_number': 1,
        'quantity': 5,
        
        
        "invoice": 5555,
        "notify_url": "http://www.example.com/your-ipn-location/",
        "return_url": "http://www.example.com/your-return-location/",
        "cancel_return": "http://www.example.com/your-cancel-location/",

    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render_to_response("payments/paypal-single.html", locals())


def recurring_payment(request):
    paypal_dict = {
        "cmd": "_xclick-subscriptions",
        "business": "your_account@paypal",
        "a3": "9.99",                      # monthly price 
        "p3": 1,                           # duration of each unit (depends on unit)
        "t3": "M",                         # duration unit ("M for Month")
        "src": "1",                        # make payments recur
        "sra": "1",                        # reattempt payment on payment error
        "no_note": "1",                    # remove extra notes (optional)
        "item_name": "my cool subscription",
        "notify_url": "http://www.example.com/your-ipn-location/",
        "return_url": "http://www.example.com/your-return-location/",
        "cancel_return": "http://www.example.com/your-cancel-location/",
    }
    
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    return render_to_response("payments/paypal-recurring.html", locals())

