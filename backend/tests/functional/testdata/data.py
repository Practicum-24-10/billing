from datetime import datetime, timedelta

jwt = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4OTY5NjA5OSwianRpIjoiOGUyZmRiOGMtN2MyZi00OGI0LWJiOGMtOWIyYmI2NWFmOTg2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjkyMzM2ZDg0LWUzOWQtNGM0My1hNDBiLTU2NTgyMTU1MWIyMSIsIm5iZiI6MTY4OTY5NjA5OSwicGVybWlzc2lvbnMiOltdLCJpc19zdXBlcnVzZXIiOmZhbHNlLCJwcl91dWlkIjoiMTNhZGMxNWUtYzNhZi00NzY5LWIxYzQtMTJjN2VlNzljYmE2IiwiZGV2aWNlX2lkIjoiOTYzNjQ5NGItOWQ3MC00M2JhLTljYzItZGZjZjAxYTY2ZTk2In0.Ljft_BCjRDmBZ4aHI-jSqZS42aIq1iKgLZAVmzVmHtSyv1lqvgLOJg8vvfrW84wiT1qOwdDSrdCIhMJsS0aBcU6ujGD_l0YdQzi1SqDImeQtfz39qE-hZ3lJVoDbVgVnOb3H6KEmCOoQFXYqrKyZ3A2eje0GIb_jdgTsNq8AcbpRDYlR-1GNgy4OlKUC0ZshClJMrKUZ_8lB0aJApWC-M5aUYFI1sWCVaDOJsReKQmnejDstvikIPKwE0TpYRyy0Oplxhpx3PQ466NV5GMQLs7aNS_lM9vCUGHpuvgjFq2_GQTHlAuMJXlJ_5DMpERvAkm8hR2CDES9ilFYMv_O9zZy__TM5bTW7AZf21N6YCttB3xtpyIGXpvclW1j4B2owwXeBYkko8yf1_9gnMJHKuZ-AHRhzinr6Ji8sQEmBJ_h_Hwy0IiMWPjv2XnC6XE7A1WoSG8rN6rb0QbpJgW64ZHL5UNR16QCH3noIONveU2Iy_ddcWZ4MfLa-tBhxzwLL80tl0PJXhwlz1uvc2WuHxzKsEPsXBZgKh9l20ctw7lH0OMw4D1a6yEEDU5-6gA-KqfA7Lm3zdOV-u1bULGW-Juju2G6ub69nVvIAJELmk9hdUdB_fdlYqXm8oTn3cxjUeq2kxrlZE_0gpag7jXCQvPJCVAWi9kGuF1vjlrt6rTA"  # noqa

payment = [
    {
        "id": "b087df75-afff-43c3-9827-1903ea7d1baa",
        "created_at": datetime.now() - timedelta(days=30),
        "kassa_payment_id": "2ca6b692-000f-5000-9000-10b66dc7da42",
        "payment_status": "succeeded",
        "users_subscriptions_id": "aee74e9d-a76a-422c-82cc-b91ff50e11c8",
    },
    {
        "id": "7226689d-de8d-4efe-af64-7b3bfd2879bb",
        "created_at": datetime.now(),
        "kassa_payment_id": "2ca6b740-000f-5000-8000-1bc4f85b3e3c",
        "payment_status": "succeeded",
        "users_subscriptions_id": "d782256f-e86c-4ec9-8baa-c7de11514273",
    },
    {
        "id": "9bb6157a-e928-4d45-aa35-f2bc0c4c5bc2",
        "created_at": datetime.now() - timedelta(days=31),
        "kassa_payment_id": "2127489d-7045-4a3c-9309-f1ce57c37bf3",
        "payment_status": "canceled",
        "users_subscriptions_id": "aee74e9d-a76a-422c-82cc-b91ff50e11c8",
    },
]

payment_method = [
    {
        "id": "f02a124b-ecf5-4e38-8c03-d03155cc82e2",
        "kassa_payment_method_id": "2caccbfc-000f-5000-a000-106cc0d44c98",
        "card_type": "MasterCard",
        "first_numbers": 555555,
        "last_numbers": 4444,
    },
    {
        "id": "6f6e6052-b23d-4149-98a1-c59a6a8c96a7",
        "kassa_payment_method_id": "2cacccdf-000f-5000-a000-1b245c9b98fb",
        "card_type": "MasterCard",
        "first_numbers": 555555,
        "last_numbers": 4477,
    },
]

subscription = [
    {
        "id": "94791a79-42a0-46cc-b231-9d8f61569b47",
        "duration": 30,
        "amount": 300.0,
        "title": "HD",
        "currency": "RUB",
        "active": True,
        "permission": "hd",
    },
    {
        "id": "b0ec64e6-3c55-4f1f-8d1b-3c9048e53a0b",
        "duration": 30,
        "amount": 500.0,
        "title": "FullHD",
        "currency": "RUB",
        "active": True,
        "permission": "fullhd",
    },
    {
        "id": "c4326b05-0e88-4c2a-a053-e8f1dd190b38",
        "duration": 30,
        "amount": 1000.0,
        "title": "4K",
        "currency": "RUB",
        "active": True,
        "permission": "4k",
    },
]

user = [{"id": "92336d84-e39d-4c43-a40b-565821551b21", "active": True}]

users_payment_method = [
    {
        "id": "ef8fe5aa-935c-4099-8f76-a45a74357999",
        "user_id": "92336d84-e39d-4c43-a40b-565821551b21",
        "payment_method_id": "f02a124b-ecf5-4e38-8c03-d03155cc82e2",
        "order": 0,
    },
    {
        "id": "624c9d41-721f-4ff4-a217-06d67f1bc779",
        "user_id": "92336d84-e39d-4c43-a40b-565821551b21",
        "payment_method_id": "6f6e6052-b23d-4149-98a1-c59a6a8c96a7",
        "order": 1,
    },
]

users_subscriptions = [
    {
        "id": "aee74e9d-a76a-422c-82cc-b91ff50e11c8",
        "user_id": "92336d84-e39d-4c43-a40b-565821551b21",
        "created_at": datetime.now() - timedelta(days=30),
        "subscription_id": "94791a79-42a0-46cc-b231-9d8f61569b47",
        "next_subscription_id": "94791a79-42a0-46cc-b231-9d8f61569b47",
        "start_at": datetime.now() - timedelta(days=30),
        "expires_at": datetime.now(),
    },
    {
        "id": "d782256f-e86c-4ec9-8baa-c7de11514273",
        "user_id": "92336d84-e39d-4c43-a40b-565821551b21",
        "created_at": datetime.now(),
        "subscription_id": "94791a79-42a0-46cc-b231-9d8f61569b47",
        "next_subscription_id": "94791a79-42a0-46cc-b231-9d8f61569b47",
        "start_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(days=30),
    },
]
