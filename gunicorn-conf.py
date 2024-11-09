import multiprocessing

from transaction_service import settings
from transaction_service.settings.logging import LOG_CONFIG

workers_per_core = 2
cores = multiprocessing.cpu_count()
default_web_concurrency = workers_per_core * cores
web_concurrency = max(int(default_web_concurrency), 2)


# Gunicorn config variables
bind = f'0.0.0.0: {settings.PORT}'
workers = web_concurrency
graceful_timeout = 30
timeout = 60
keepalive = 2
logconfig_dict = LOG_CONFIG
