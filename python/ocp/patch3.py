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

# The payload to add an environment variable to all containers
new_env_var = {
    "name": "NEW_ENV_VAR_FROM_FIELD_REF",
    "valueFrom": {
        "fieldRef": {
            "fieldPath": "metadata.name"
        }
    }
}

# Fetch the existing deployment first
response = requests.get(url, headers=headers, verify=False)  # verify=False is insecure; use only for testing

if response.status_code == 200:
    deployment = response.json()
    
    # Loop through all containers and add the new environment variable
    for container in deployment["spec"]["template"]["spec"]["containers"]:
        if "env" in container:
            container["env"].append(new_env_var)
        else:
            container["env"] = [new_env_var]
    
    # Make the PATCH API request to update the deployment
    patch_payload = {
        "spec": deployment["spec"]
    }
    
    patch_response = requests.patch(url, headers=headers, data=json.dumps(patch_payload), verify=False)  # verify=False is insecure; use only for testing
    
    # Check for a successful response
    if patch_response.status_code == 200:
        print(f"Successfully updated deployment: {deployment_name}")
    else:
        print(f"Failed to update deployment: {patch_response.content}")
else:
    print(f"Failed to get existing deployment: {response.content}")
