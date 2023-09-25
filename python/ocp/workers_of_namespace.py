import openshift

# Initialize API client
api = openshift.OapiApi() 

# Get deployments in namespace
deployments = api.list_deployment_for_all_namespaces(namespace='mynamespace')

# Track unique workers
workers = []

# Loop through deployments
for deployment in deployments:

  # Get pods for deployment
  pods = api.list_namespaced_pod(namespace='mynamespace', label_selector=f'deployment={deployment.metadata.name}')

  # Loop through pods
  for pod in pods.items:

    # Check if worker is already tracked
    if pod.spec.node_name not in workers:
    
      # Add new worker to list
      workers.append(pod.spec.node_name) 
      
# Print unique workers
print(workers)
