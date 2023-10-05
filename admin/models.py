from sqladmin import ModelView

from admin.config import translation as _
from database.models import (
    Payment,
    PaymentMethod,
    Subscription,
    User,
    UsersPaymentMethods,
    UsersSubscriptions,
)


class SubscriptionAdmin(ModelView, model=Subscription):
    name = _("Subscription")
    name_plural = _("Subscriptions")
    column_labels = {
        Subscription.title: _("Title"),
        Subscription.active: _("Active"),
        Subscription.amount: _("Amount"),
        Subscription.currency: _("Currency"),
        Subscription.duration: _("Duration"),
        Subscription.permission: _("Permission"),
        Subscription.users_subscriptions: _("User subscriptions"),
        Subscription.users_next_subscriptions: _("Next user subscriptions"),
    }

    exclude_list = [
        Subscription.users_subscriptions,
        Subscription.users_next_subscriptions,
        Subscription.id,
    ]

    form_excluded_columns = exclude_list

    column_details_exclude_list = exclude_list

    column_exclude_list = exclude_list


class UserAdmin(ModelView, model=User):
    name = _("User")
    name_plural = _("Users")
    column_list = "__all__"
    column_labels = {
        User.id: _("id"),
        User.active: _("Active"),
        User.subscriptions: _("Subscriptions"),
        User.payment_methods: _("Payment methods"),
    }


class UsersSubscriptionsAdmin(ModelView, model=UsersSubscriptions):
    name = _("User Subscriptions")
    name_plural = _("Users Subscriptions")
    column_labels = {
        UsersSubscriptions.user: _("User"),
        UsersSubscriptions.subscription: _("Subscription"),
        UsersSubscriptions.next_subscription: _("Next subscription"),
        UsersSubscriptions.payment: _("Payment"),
        UsersSubscriptions.created_at: _("Created at"),
        UsersSubscriptions.start_at: _("Start at"),
        UsersSubscriptions.expires_at: _("Expires at"),
    }

    exclude_list = [
        UsersSubscriptions.id,
        UsersSubscriptions.user_id,
        UsersSubscriptions.subscription_id,
        UsersSubscriptions.next_subscription_id,
    ]

    column_details_exclude_list = exclude_list

    form_excluded_columns = exclude_list

    column_exclude_list = exclude_list


class PaymentAdmin(ModelView, model=Payment):
    name = _("Payment")
    name_plural = _("Payments")
    column_labels = {
        Payment.users_subscription: _("User subscription"),
        Payment.id: _("id"),
        Payment.created_at: _("Created at"),
        Payment.kassa_payment_id: _("Kassa payment id"),
        Payment.payment_status: _("Payment status"),
    }

    exclude_list = [
        Payment.users_subscriptions_id,
    ]

    column_details_exclude_list = exclude_list

    form_excluded_columns = exclude_list

    column_exclude_list = exclude_list


class UsersPaymentMethodsAdmin(ModelView, model=UsersPaymentMethods):
    name = _("User payment method")
    name_plural = _("User payment methods")
    column_labels = {
        UsersPaymentMethods.user: _("User"),
        UsersPaymentMethods.payment_method: _("Payment method"),
        UsersPaymentMethods.id: _("id"),
        UsersPaymentMethods.order: _("Order"),
    }

    exclude_list = [
        UsersPaymentMethods.user_id,
        UsersPaymentMethods.payment_method_id,
    ]

    column_details_exclude_list = exclude_list

    form_excluded_columns = exclude_list

    column_exclude_list = exclude_list


class PaymentMethodAdmin(ModelView, model=PaymentMethod):
    can_edit = False
    can_create = False
    name = _("Payment method")
    name_plural = _("Payment methods")
    column_labels = {
        PaymentMethod.user_payment_method: _("User payment method"),
        PaymentMethod.id: _("id"),
        PaymentMethod.kassa_payment_method_id: _("Kassa payment method id"),
        PaymentMethod.card_type: _("Card type"),
        PaymentMethod.first_numbers: _("First numbers"),
        PaymentMethod.last_numbers: _("Last numbers"),
    }
