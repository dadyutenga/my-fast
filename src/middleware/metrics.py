from fastapi import Request, Response
from fastapi.routing import APIRoute
import time
import json

from src.routers.metrics import metrics_data

class MetricsMiddleware:
    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time

        # Update metrics
        metrics_data['request_count'] += 1
        endpoint = request.url.path
        if endpoint not in metrics_data['endpoint_stats']:
            metrics_data['endpoint_stats'][endpoint] = {'count': 0, 'total_time': 0, 'errors': 0}
        metrics_data['endpoint_stats'][endpoint]['count'] += 1
        metrics_data['endpoint_stats'][endpoint]['total_time'] += process_time
        if response.status_code >= 400:
            metrics_data['error_count'] += 1
            metrics_data['endpoint_stats'][endpoint]['errors'] += 1

        return response
