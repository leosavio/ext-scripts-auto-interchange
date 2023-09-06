import requests
import json

# Initialize variables
namespace = "your-namespace-here"
deployment_name = "your-deployment-name-here"
url = f"https://api.your-openshift-cluster.com/apis/apps/v1/namespaces/{namespace}/deployments/{deployment_name}"
token = "your-token-here"

# Headers for the API request
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/merge-patch+json"
}

# The payload to update metadata:labels
payload = {
    "metadata": {
        "labels": {
            "new-label-key": "new-label-value"
        }
    }
}

# Make the PATCH API request
response = requests.patch(url, headers=headers, data=json.dumps(payload), verify=False)  # verify=False is insecure; use only for testing

# Check for a successful response
if response.status_code == 200:
    print(f"Successfully updated deployment: {deployment_name}")
else:
    print(f"Failed to update deployment: {response.content}")
