import subprocess
import json

def get_pods_on_nodes(namespace):
    # Get list of deployments in the namespace
    deployments_output = subprocess.check_output(['oc', 'get', 'deploy', '-n', namespace, '-o', 'json'])
    deployments = json.loads(deployments_output)

    result = {}
    
    for deployment in deployments['items']:
        deployment_name = deployment['metadata']['name']
        
        # Get pods for each deployment
        pods_output = subprocess.check_output(['oc', 'get', 'pods', '-n', namespace, '-l', f'app={deployment_name}', '-o', 'json'])
        pods = json.loads(pods_output)

        for pod in pods['items']:
            pod_name = pod['metadata']['name']
            node_name = pod['spec']['nodeName']

            if node_name not in result:
                result[node_name] = []
            result[node_name].append(pod_name)
            
    return result

namespace = 'your-namespace'
pods_on_nodes = get_pods_on_nodes(namespace)

for node, pods in pods_on_nodes.items():
    print(f"Node: {node}")
    for pod in pods:
        print(f"  - {pod}")
