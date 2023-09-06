import requests
from kubernetes import config, client

# Initialize OpenShift API client
config.load_kube_config()
api_instance = client.CustomObjectsApi()

# OpenShift REST API URL for listing deployments in a specific namespace
namespace = "your-namespace-here"
url = f"https://api.your-openshift-cluster.com/apis/apps/v1/namespaces/{namespace}/deployments"

# Your OpenShift token for authentication
token = "your-token-here"

# Headers for the API request
headers = {
    "Authorization": f"Bearer {token}"
}

# Make the API request
response = requests.get(url, headers=headers, verify=False)  # verify=False is insecure; use only for testing

# Check for a successful response
if response.status_code == 200:
    deployments = response.json()["items"]
    for deployment in deployments:
        deployment_name = deployment["metadata"]["name"]
        match_labels = deployment["spec"]["selector"]["matchLabels"]
        print(f"Deployment Name: {deployment_name}")
        print(f"Match Labels: {match_labels}")
        print("------")
else:
    print(f"Failed to get deployments: {response.content}")
