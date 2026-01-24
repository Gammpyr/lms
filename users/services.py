import os

import stripe

stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_stripe_product(product_name):
    """Создаёт продукт в Stripe"""
    product = stripe.Product.create(name=f"Курс {product_name}")

    return product


def create_stripe_price(product, amount):
    """Создаёт цену в Stripe"""
    # product_id = stripe.Product.retrieve(product_id)
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": product.get("name")},
    )

    return price


def create_stripe_session(price):
    """Создаёт сессию в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session
