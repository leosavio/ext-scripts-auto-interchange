import subprocess
import json

def get_nodes_from_machineset(machineset_name):
    # Get nodes from a specific MachineSet
    nodes_output = subprocess.check_output(['oc', 'get', 'nodes', '-l', f'machine.openshift.io/machineset={machineset_name}', '-o', 'json'])
    nodes = json.loads(nodes_output)
    return [(node['metadata']['name'], machineset_name) for node in nodes['items']]

def get_pods_on_nodes(exclude_namespace):
    # List all pods across all namespaces, excluding OpenShift namespaces and the specific namespace
    pods_output = subprocess.check_output(['oc', 'get', 'pods', '--all-namespaces', '-o', 'json'])
    pods = json.loads(pods_output)

    result = {}
    for pod in pods['items']:
        namespace = pod['metadata']['namespace']
        if namespace.startswith('openshift-') or namespace == exclude_namespace:
            continue
        
        pod_name = pod['metadata']['name']
        node_name = pod['spec']['nodeName']

        if node_name not in result:
            result[node_name] = []
        result[node_name].append((namespace, pod_name))
        
    return result

# 1. List MachineSets containing the string 'ma'
machinesets_output = subprocess.check_output(['oc', 'get', 'machinesets', '-n', 'openshift-machine-api', '-o', 'json'])
machinesets = json.loads(machinesets_output)

filtered_node_machinesets = []
for machineset in machinesets['items']:
    if 'ma' in machineset['metadata']['name']:
        machineset_name = machineset['metadata']['name']
        filtered_node_machinesets.extend(get_nodes_from_machineset(machineset_name))

# 2 & 3. List pods running on these nodes excluding a specific namespace
exclude_namespace = 'your-excluded-namespace'
pods_on_nodes = get_pods_on_nodes(exclude_namespace)

# Print results
for node, machineset in filtered_node_machinesets:
    if node in pods_on_nodes:
        print(f"Node: {node} - MachineSet: {machineset}")
        for namespace, pod in pods_on_nodes[node]:
            print(f"  Namespace: {namespace} - Pod: {pod}")

