import boto3

def fetch_ec2_details(profile_name):
    session = boto3.Session(profile_name=profile_name)
    ec2 = session.resource('ec2')
    asg_client = session.client('autoscaling')

    instances_details = []

    # Fetching all instances for the given profile
    for instance in ec2.instances.all():
        instance_data = {
            'Instance ID': instance.id,
            'Instance Type': instance.instance_type,
            'Launch Time': instance.launch_time,
            'Tags': {tag['Key']: tag['Value'] for tag in instance.tags or []},
            'EBS Volumes': [vol.id for vol in instance.volumes.all()],
        }

        # Fetching ASG details for the instance
        asg_response = asg_client.describe_auto_scaling_instances(InstanceIds=[instance.id])
        if asg_response['AutoScalingInstances']:
            instance_data['ASG Name'] = asg_response['AutoScalingInstances'][0]['AutoScalingGroupName']
            instance_data['Number of Instances'] = len(asg_client.describe_auto_scaling_groups(
                AutoScalingGroupNames=[instance_data['ASG Name']])['AutoScalingGroups'][0]['Instances'])
        else:
            instance_data['ASG Name'] = None
            instance_data['Number of Instances'] = 1

        instances_details.append(instance_data)

    return instances_details
