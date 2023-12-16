#!/bin/bash

# Get all pods and their nodes
pods_and_nodes=$(oc get pods -o=custom-columns=NAME:.metadata.name,NODE:.spec.nodeName --no-headers)

# Iterate over each pod and its node
echo "Pod,Node,Machine,MachineSet"
while IFS= read -r line; do
    pod_name=$(echo $line | awk '{print $1}')
    node_name=$(echo $line | awk '{print $2}')

    # Find the corresponding machine for the node
    machine_name=$(oc get machine -o=custom-columns=NAME:.metadata.name,NODE:.status.nodeRef.name --no-headers | grep $node_name | awk '{print $1}')

    # Find the machine set for the machine
    machine_set_name=$(oc get machineset -o=custom-columns=NAME:.metadata.name,MACHINE:.spec.template.metadata.labels --no-headers | grep $machine_name | awk '{print $1}')

    # Print the pod, node, machine, and machine set
    echo "$pod_name,$node_name,$machine_name,$machine_set_name"
done <<< "$pods_and_nodes"
