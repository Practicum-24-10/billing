import time
import uuid

from yookassa import Configuration, Payment
from yookassa.domain.exceptions import BadRequestError

Configuration.account_id = "255446"
Configuration.secret_key = "test_6J9GVY4CgQmhyd74ZaucUjNC00eZ3USpMAfBQg5yrQk"

from yookassa import Payment

try:
    payment1 = Payment.create({
        "amount": {
            "value": "6.00",
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.example.com/return_url"
        },
        "capture": False,
        "description": "Заказ №72",
        "save_payment_method": True
    }, 1)
except BadRequestError as e:
    print(type(e))
    error_description = e
    print(error_description.args[0]['description'])

pass
print(payment1.confirmation.confirmation_url)
# response = Payment.cancel(
#   payment1.id
# )
# pass
#
# payment_id = '2c9a4ee2-000f-5000-9000-1921e0fb81aa'
t = time.time()
payment = Payment.create({
    "amount": {
        "value": "2.00",
        "currency": "RUB"
    },
    "capture": False,
    "payment_method_id": '2c9a4ee2-000f-5000-9000-1921e0fb81aa',
    "description": "Заказ №37",
    "metadata": {
        "user_id": "qwerrtfdaswqewregfd"
    }
})
t2 = time.time()
print(t2 - t)
