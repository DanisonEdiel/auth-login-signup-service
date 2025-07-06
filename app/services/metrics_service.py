import time
import json
from datetime import datetime
import requests
from loguru import logger

from app.core.config import settings


class GrafanaMetricsService:
    """
    Service for sending metrics to Grafana Cloud
    """
    
    def __init__(self):
        self.enabled = settings.GRAFANA_ENABLED
        # Configuración para Grafana Cloud
        self.base_url = f"https://{settings.GRAFANA_HOST}"
        self.api_key = settings.GRAFANA_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.app_name = settings.PROJECT_NAME
        self.environment = settings.ENVIRONMENT
        self.metrics = {}
        
    def initialize(self):
        """
        Initialize metrics service
        """
        if not self.enabled:
            logger.info("Grafana metrics disabled")
            return
            
        try:
            # Verificar que podemos conectarnos a Grafana Cloud
            response = requests.get(
                f"{self.base_url}/api/health",
                headers=self.headers,
                timeout=5
            )
            
            if response.status_code == 200:
                logger.info("Connected to Grafana Cloud successfully")
            else:
                logger.warning(f"Grafana Cloud health check failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Failed to connect to Grafana Cloud: {str(e)}")
            
        # Registrar inicio de la aplicación
        self._send_annotation({
            "text": "Application started",
            "tags": ["startup", self.app_name, self.environment]
        })
            
    def record_login(self, user_id: str, success: bool):
        """
        Record login attempt
        """
        if not self.enabled:
            return
            
        timestamp = int(time.time() * 1000)
        
        try:
            # Enviar métrica de login a Grafana Cloud
            metric_data = {
                "name": "auth_login",
                "value": 1,
                "timestamp": timestamp,
                "tags": [
                    {"key": "user_id", "value": user_id},
                    {"key": "success", "value": str(success).lower()},
                    {"key": "service", "value": self.app_name},
                    {"key": "environment", "value": self.environment}
                ]
            }
            
            self._send_metric(metric_data)
            
            # Si el login fue exitoso, enviar una anotación
            if success:
                self._send_annotation({
                    "text": f"User {user_id} logged in successfully",
                    "tags": ["login", "success", self.app_name]
                })
            
        except Exception as e:
            logger.error(f"Failed to record login metric: {str(e)}")
            
    def record_request(self, method: str, path: str, status_code: int, duration_ms: float):
        """
        Record API request
        """
        if not self.enabled:
            return
            
        timestamp = int(time.time() * 1000)
        
        try:
            # Enviar métrica de solicitud a Grafana Cloud
            request_metric = {
                "name": "http_request",
                "value": 1,
                "timestamp": timestamp,
                "tags": [
                    {"key": "method", "value": method},
                    {"key": "path", "value": path},
                    {"key": "status_code", "value": str(status_code)},
                    {"key": "service", "value": self.app_name},
                    {"key": "environment", "value": self.environment}
                ]
            }
            
            self._send_metric(request_metric)
            
            # Enviar métrica de duración
            duration_metric = {
                "name": "http_request_duration_ms",
                "value": duration_ms,
                "timestamp": timestamp,
                "tags": [
                    {"key": "method", "value": method},
                    {"key": "path", "value": path},
                    {"key": "status_code", "value": str(status_code)},
                    {"key": "service", "value": self.app_name},
                    {"key": "environment", "value": self.environment}
                ]
            }
            
            self._send_metric(duration_metric)
            
            # Si es un error (4xx o 5xx), enviar una anotación
            if status_code >= 400:
                self._send_annotation({
                    "text": f"Error {status_code} on {method} {path}",
                    "tags": ["error", f"status-{status_code}", self.app_name]
                })
            
        except Exception as e:
            logger.error(f"Failed to record request metric: {str(e)}")
            
    def _send_metric(self, metric_data):
        """
        Send metric to Grafana Cloud
        """
        if not self.api_key:
            logger.warning("Grafana API key not configured, skipping metric")
            return
            
        try:
            # Formato para Grafana Cloud
            payload = {
                "metrics": [{
                    "name": metric_data["name"],
                    "value": metric_data["value"],
                    "timestamp": metric_data["timestamp"],
                    "tags": metric_data["tags"]
                }]
            }
            
            # Enviar a Grafana Cloud
            response = requests.post(
                f"{self.base_url}/api/v1/metrics",
                headers=self.headers,
                json=payload,
                timeout=5
            )
            
            if response.status_code not in (200, 201, 202):
                logger.warning(f"Failed to send metric to Grafana Cloud: {response.status_code} - {response.text}")
            else:
                logger.debug(f"Metric sent successfully to Grafana Cloud: {metric_data['name']}")
                
        except Exception as e:
            logger.error(f"Error sending metric to Grafana Cloud: {str(e)}")
            
    def _send_annotation(self, annotation_data):
        """
        Send annotation to Grafana Cloud
        """
        if not self.api_key:
            logger.warning("Grafana API key not configured, skipping annotation")
            return
            
        try:
            # Formato para anotaciones de Grafana
            payload = {
                "text": annotation_data["text"],
                "tags": annotation_data["tags"],
                "time": int(time.time() * 1000),
                "timeEnd": int(time.time() * 1000)
            }
            
            # Enviar a Grafana Cloud
            response = requests.post(
                f"{self.base_url}/api/annotations",
                headers=self.headers,
                json=payload,
                timeout=5
            )
            
            if response.status_code not in (200, 201, 202):
                logger.warning(f"Failed to send annotation to Grafana Cloud: {response.status_code} - {response.text}")
            else:
                logger.debug(f"Annotation sent successfully to Grafana Cloud: {annotation_data['text']}")
                
        except Exception as e:
            logger.error(f"Error sending annotation to Grafana Cloud: {str(e)}")


# Singleton instance
metrics_service = GrafanaMetricsService()
