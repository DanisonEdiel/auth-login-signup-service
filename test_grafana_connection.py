import requests
import sys

def test_grafana_connection(host, api_key):
    """Test connection to Grafana Cloud"""
    try:
        # Construct base URL
        base_url = f"https://{host}"
        
        # Set headers with API key
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        print(f"Testing connection to Grafana Cloud: {base_url}")
        
        # Test health endpoint
        health_url = f"{base_url}/api/health"
        print(f"Checking health endpoint: {health_url}")
        
        health_response = requests.get(health_url, headers=headers, timeout=10)
        print(f"Health check status code: {health_response.status_code}")
        print(f"Health check response: {health_response.text}")
        
        # Test annotations endpoint
        annotations_url = f"{base_url}/api/annotations"
        print(f"\nChecking annotations endpoint: {annotations_url}")
        
        annotations_response = requests.get(annotations_url, headers=headers, timeout=10)
        print(f"Annotations check status code: {annotations_response.status_code}")
        
        # Test dashboards endpoint
        dashboards_url = f"{base_url}/api/dashboards"
        print(f"\nChecking dashboards endpoint: {dashboards_url}")
        
        dashboards_response = requests.get(f"{dashboards_url}/home", headers=headers, timeout=10)
        print(f"Dashboards check status code: {dashboards_response.status_code}")
        
        if health_response.status_code == 200:
            print("\nGrafana Cloud connection successful!")
            return True
        else:
            print("\nFailed to connect to Grafana Cloud")
            return False
            
    except Exception as e:
        print(f"Error connecting to Grafana Cloud: {e}")
        return False

if __name__ == "__main__":
    # Grafana connection parameters
    host = "danisonediel.grafana.net"
    
    # Get API key from user input for security
    api_key = input("Enter your Grafana API key: ")
    
    # Test the connection
    success = test_grafana_connection(host, api_key)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
