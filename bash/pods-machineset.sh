#!/bin/bash

# Get all pods and their nodes
pods_and_nodes=$(oc get pods -o=custom-columns=NAME:.metadata.name,NODE:.spec.nodeName --no-headers)

echo "Pod,Node,Machine,MachineSet"

# Iterate over each pod and its node
while IFS= read -r line; do
    pod_name=$(echo $line | awk '{print $1}')
    node_name=$(echo $line | awk '{print $2}')

    # Find the corresponding machine for the node
    machine_name=$(oc get machine -o=custom-columns=NAME:.metadata.name,NODE:.status.nodeRef.name --no-headers | grep $node_name | awk '{print $1}')

    # Assuming machines are labeled with their machine set's name
    machine_set_label=$(oc get machine $machine_name -o jsonpath='{.metadata.labels.machine\.openshift\.io/cluster-api-machineset}')

    # Print the pod, node, machine, and machine set
    echo "$pod_name,$node_name,$machine_name,$machine_set_label"
done <<< "$pods_and_nodes"
