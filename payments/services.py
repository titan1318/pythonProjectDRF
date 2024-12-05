import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY

def create_stripe_product(name):
    return stripe.Product.create(name=name)

def create_stripe_price(product_id, amount):
    return stripe.Price.create(
        product=product_id,
        unit_amount=amount,
        currency='usd',
    )

def create_stripe_session(price_id):
    return stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://yourdomain.com/success',
        cancel_url='https://yourdomain.com/cancel',
    )

def retrieve_stripe_session(session_id):
    return stripe.checkout.Session.retrieve(session_id)
