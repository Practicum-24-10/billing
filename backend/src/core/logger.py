import logging

from starlette_context import context


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        if context.exists() and "X-Request-ID" in context.data:
            record.request_id = context.data["X-Request-ID"]
        else:
            record.request_id = "none"
        return True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "custom_filter": {
            "()": RequestIdFilter,
        }
    },
    "formatters": {
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(asctime)s :: "
            '%(client_addr)s - "%(request_line)s" %(status_code)s',
        },
    },
    "handlers": {
        "logstash": {
            "level": "INFO",
            "class": "logstash.LogstashHandler",
            "filters": ["custom_filter"],
            "host": "logstash",
            "port": 5044,
            "version": 1,
            "message_type": "logstash",
            "fqdn": False,
            "tags": ["ugc"],
        },
    },
    "loggers": {
        "uvicorn.error": {
            "propagate": True,
        },
        "uvicorn.access": {"propagate": True},
    },
    "root": {"level": "INFO", "handlers": ["logstash"]},
}
