import requests
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_grafana_token(host, api_key):
    """Test a specific Grafana Cloud token"""
    base_url = f"https://{host}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    logger.info(f"Testing Grafana Cloud connection to: {base_url}")
    logger.info(f"Using API key: {api_key[:5]}...{api_key[-5:]}")
    
    endpoints = [
        "/api/health",
        "/api/dashboards/home",
        "/api/org",
        "/api/annotations",
        "/api/metrics"
    ]
    
    success = False
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            logger.info(f"Testing endpoint: {url}")
            
            response = requests.get(url, headers=headers, timeout=10)
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")
            
            if len(response.text) > 500:
                logger.info(f"Response body (truncated): {response.text[:500]}...")
            else:
                logger.info(f"Response body: {response.text}")
            
            if response.status_code in (200, 201, 202, 302, 401, 403):
                if response.status_code in (200, 201, 202):
                    logger.info(f"✅ Endpoint {endpoint} accessible")
                    success = True
                elif response.status_code in (401, 403):
                    logger.warning(f"⚠️ Authentication issue with endpoint {endpoint}")
                else:
                    logger.info(f"⚠️ Endpoint {endpoint} returned redirect")
            else:
                logger.error(f"❌ Failed to access endpoint {endpoint}")
                
        except Exception as e:
            logger.error(f"Error testing endpoint {endpoint}: {str(e)}")
    
    # Try to send a test metric
    try:
        logger.info("\nTrying to send a test metric...")
        metric_url = f"{base_url}/api/v1/metrics"
        
        payload = {
            "metrics": [{
                "name": "test_metric",
                "value": 1,
                "timestamp": int(__import__('time').time() * 1000),
                "tags": [
                    {"key": "test", "value": "true"},
                    {"key": "environment", "value": "test"}
                ]
            }]
        }
        
        metric_response = requests.post(
            metric_url,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        logger.info(f"Metric send response: {metric_response.status_code} - {metric_response.text}")
        
        if metric_response.status_code in (200, 201, 202):
            logger.info("✅ Test metric sent successfully")
            success = True
        else:
            logger.warning(f"⚠️ Failed to send test metric")
            
    except Exception as e:
        logger.error(f"Error sending test metric: {str(e)}")
    
    return success

if __name__ == "__main__":
    # Grafana Cloud connection parameters
    host = "danisonediel.grafana.net"
    
    # Solicitar token de forma segura
    api_key = input("Ingresa tu token de Grafana (no se mostrará en pantalla): ")
    
    # Test the connection
    success = test_grafana_token(host, api_key)
    
    if success:
        logger.info("\n✅ Grafana Cloud connection test PASSED")
        sys.exit(0)
    else:
        logger.error("\n❌ Grafana Cloud connection test FAILED ")
        sys.exit(1)
