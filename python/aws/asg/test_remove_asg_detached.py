import boto3
import datetime

def get_asg_instances(asg_name):
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    instances = response['AutoScalingGroups'][0]['Instances']
    return [instance['InstanceId'] for instance in instances]

def get_all_instances():
    client = boto3.client('ec2')
    response = client.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance)
    return instances

def is_instance_detached(instance_id):
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_instances(InstanceIds=[instance_id])
    return len(response['AutoScalingInstances']) == 0

def change_termination_protection(instance_id, protection_enabled):
    client = boto3.client('ec2')
    response = client.modify_instance_attribute(
        InstanceId=instance_id,
        DisableApiTermination={'Value': protection_enabled}
    )
    return response

def terminate_instance(instance_id):
    client = boto3.client('ec2')
    response = client.terminate_instances(InstanceIds=[instance_id])
    return response

def get_instance_launch_time(instance):
    launch_time_str = instance['LaunchTime']
    launch_time = datetime.datetime.strptime(launch_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
    return launch_time

def is_instance_old_enough(instance, threshold_hours):
    launch_time = get_instance_launch_time(instance)
    now = datetime.datetime.utcnow()
    age = now - launch_time
    return age.total_seconds() / 3600 >= threshold_hours

def get_asg_names():
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups()
    asg_names = [asg['AutoScalingGroupName'] for asg in response['AutoScalingGroups']]
    return asg_names

def get_instances_by_asg_name(asg_name):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [asg_name]}])
    return list(instances)

if __name__ == "__main__":
    threshold_hours = 24

    log = []

    all_asg_names = get_asg_names()

    for asg_name in all_asg_names:
        instances_with_same_name = get_instances_by_asg_name(asg_name)
        asg_instances = get_asg_instances(asg_name)

        for instance in instances_with_same_name:
            instance_id = instance.id

            if instance_id in asg_instances:
                continue  # Skip instances that are part of Auto Scaling Groups

            if is_instance_detached(instance_id):
                launch_time = get_instance_launch_time(instance)
                if is_instance_old_enough(instance, threshold_hours):
                    log.append(f"Terminating instance {instance_id} (launch time: {launch_time})")
                    # Uncomment the line below to actually terminate the instance
                    # terminate_instance(instance_id)
                else:
                    log.append(f"Skipping instance {instance_id} (launch time: {launch_time})")

    # Print the log with all actions and skipped instances
    for entry in log:
        print(entry)