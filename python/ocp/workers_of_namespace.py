import openshift

# Connect to OpenShift API 
api = openshift.client.ApiClient()

# Get deployments
deployments = api.list_deployment_for_all_namespaces(namespace='mynamespace')

# Track unique workers
workers = [] 

# Loop through deployments
for deployment in deployments:

  # Get pods
  pods = deployment.pods
  
  # Loop through pods
  for pod in pods:
  
    # Check if worker is already in list
    if pod.node not in workers:
    
      # Add worker to list
      workers.append(pod.node)
      
# Print unique workers      
print(workers)
