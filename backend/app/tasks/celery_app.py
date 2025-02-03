from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

celery_app.conf.update(
    task_routes={
        "tasks.orders.*": {"queue": "orders_queue"},
    }
)
celery_app.autodiscover_tasks(["app.models"])