from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as _UUID
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[UUID] = mapped_column(_UUID, primary_key=True, default=uuid4())
    active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    subscriptions: Mapped[list["UsersSubscriptions"]] = relationship(
        "UsersSubscriptions", back_populates="user"
    )
    payment_methods: Mapped[list["UsersPaymentMethods"]] = relationship(
        "UsersPaymentMethods", back_populates="user"
    )


class UsersPaymentMethods(Base):
    __tablename__ = "users_payment_method"
    id: Mapped[UUID] = mapped_column(_UUID, primary_key=True, default=uuid4())
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="payment_methods")
    payment_method_id: Mapped[UUID] = mapped_column(
        ForeignKey("payment_method.id"), nullable=False
    )
    payment_method: Mapped["PaymentMethod"] = relationship(
        "PaymentMethod", back_populates="user_payment_method"
    )
    order: Mapped[int] = mapped_column(Integer, nullable=False)


class PaymentMethod(Base):
    __tablename__ = "payment_method"
    id: Mapped[UUID] = mapped_column(_UUID, primary_key=True, default=uuid4())
    kassa_payment_method_id: Mapped[str] = mapped_column(String, nullable=False)
    user_payment_method: Mapped["UsersPaymentMethods"] = relationship(
        "UsersPaymentMethods", back_populates="payment_method"
    )


class Subscription(Base):
    __tablename__ = "subscription"
    id: Mapped[UUID] = mapped_column(_UUID, primary_key=True, default=uuid4())
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    permission: Mapped[str] = mapped_column(String, nullable=False)
    users_subscriptions: Mapped[list["UsersSubscriptions"]] = relationship(
        "UsersSubscriptions", back_populates="subscription",
        foreign_keys="[UsersSubscriptions.subscription_id]",
    )
    users_next_subscriptions: Mapped[list["UsersSubscriptions"]] = relationship(
        "UsersSubscriptions", back_populates="next_subscription",
        foreign_keys="[UsersSubscriptions.next_subscription_id]",
    )


class Payment(Base):
    __tablename__ = "payment"
    id: Mapped[UUID] = mapped_column(_UUID, primary_key=True, default=uuid4())
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, default=datetime.now()
    )
    kassa_payment_id: Mapped[str] = mapped_column(String, nullable=False)
    payment_status: Mapped[str] = mapped_column(String, nullable=False)

    users_subscriptions_id: Mapped[UUID] = mapped_column(
        ForeignKey("users_subscriptions.id"), nullable=False
    )
    users_subscription: Mapped["UsersSubscriptions"] = relationship(
        "UsersSubscriptions", back_populates="payment"
    )


class UsersSubscriptions(Base):
    __tablename__ = "users_subscriptions"
    id: Mapped[UUID] = mapped_column(_UUID, primary_key=True, default=uuid4())
    user_id: Mapped[UUID] = mapped_column("User", ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="subscriptions")

    subscription_id: Mapped[UUID] = mapped_column(
        ForeignKey("subscription.id"), nullable=False
    )
    next_subscription_id: Mapped[UUID] = mapped_column(
        ForeignKey("subscription.id"), nullable=False
    )

    subscription: Mapped["Subscription"] = relationship("Subscription",
                                                        back_populates="users_subscriptions",foreign_keys=[subscription_id],overlaps="subscription,users_subscriptions"
                                                        )
    next_subscription: Mapped["Subscription"] = relationship("Subscription",
                                                             back_populates="users_next_subscriptions",foreign_keys=[subscription_id],overlaps="subscription,users_subscriptions"
                                                             )

    start_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    payment: Mapped[list["UsersSubscriptions"]] = relationship(
        "Payment", back_populates="users_subscription"
    )
