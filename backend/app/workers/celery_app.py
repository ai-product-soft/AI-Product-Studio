from celery import Celery
from app.config import settings

celery_app = Celery(
    "ai_product_studio",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=[
        "app.workers.research_worker",
        "app.workers.plan_worker",
        "app.workers.generation_worker",
        "app.workers.promotion_worker",
        "app.workers.sales_worker",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    worker_prefetch_multiplier=1,
)

celery_app.conf.task_routes = {
    "app.workers.research_worker.*": {"queue": "research"},
    "app.workers.plan_worker.*": {"queue": "plan"},
    "app.workers.generation_worker.*": {"queue": "generate"},
    "app.workers.promotion_worker.*": {"queue": "promote"},
    "app.workers.sales_worker.*": {"queue": "sales"},
}
