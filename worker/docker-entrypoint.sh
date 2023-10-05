#!/bin/sh
case "$1" in
    "payments_worker")
        shift; python ./worker_payments.py $@;;
    "user_subscriptions_worker")
        shift; python ./worker_user_subscriptions.py $@;;
    *)
        echo "Unknown parameter: $@">&2; exit 1;;
esac