import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from admin.db import async_session, engine
from admin.models import (
    PaymentAdmin,
    PaymentMethodAdmin,
    SubscriptionAdmin,
    UserAdmin,
    UsersPaymentMethodsAdmin,
    UsersSubscriptionsAdmin,
)
from admin.translate import translated_strings

app = FastAPI()
admin = Admin(
    app, engine, async_session, title="Billing", templates_dir="admin/templates"
)

admin.templates.env.globals.update(translated_strings)

admin.add_view(SubscriptionAdmin)
admin.add_view(UserAdmin)
admin.add_view(UsersSubscriptionsAdmin)
admin.add_view(UsersPaymentMethodsAdmin)
admin.add_view(PaymentMethodAdmin)
admin.add_view(PaymentAdmin)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
