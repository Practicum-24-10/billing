import uuid

from yookassa import Configuration, Payment

Configuration.account_id = "255446"
Configuration.secret_key = "test_6J9GVY4CgQmhyd74ZaucUjNC00eZ3USpMAfBQg5yrQk"

from yookassa import Payment

payment = Payment.create({
    "amount": {
        "value": "2.00",
        "currency": "RUB"
    },
    "payment_method_data": {
        "type": "bank_card"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://www.example.com/return_url"
    },
    "capture": True,
    "description": "Заказ №72",
    "save_payment_method": True
})
print(payment.confirmation.confirmation_url)