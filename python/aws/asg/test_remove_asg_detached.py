# CUIDADO
# ######################################################################
# #                                                                    #
# #                        CUIDADO                                     #
# #                                                                    #
# ######################################################################
# CUIDADO
# 
# The following code is designed to terminate instances. Make sure to 
# test this thoroughly in a safe environment before running it in
# production. The termination process is irreversible and could result 
# in data loss or other unintended consequences if used improperly.
# 
# By proceeding, you acknowledge the risks involved and take full 
# responsibility for any consequences that may arise from running this 
# script.
# 
# CUIDADO


import boto3
import datetime

def get_asg_names():
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups()
    asg_names = [asg['AutoScalingGroupName'] for asg in response['AutoScalingGroups']]
    return asg_names

def get_running_instances_by_asg_name(asg_name):
    client = boto3.client('ec2')
    response = client.describe_instances(
        Filters=[
            {'Name': 'tag:Name', 'Values': [asg_name]},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance)
    return instances

def get_asg_instances(asg_name):
    client = boto3.client('autoscaling')
    response = client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg_name])
    instances = response['AutoScalingGroups'][0]['Instances']
    return [instance['InstanceId'] for instance in instances]

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
    launch_time_str = instance['LaunchTime'].strftime("%Y-%m-%dT%H:%M:%S+00:00")
    launch_time = datetime.datetime.strptime(launch_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
    return launch_time

def is_instance_old_enough(instance, threshold_hours):
    launch_time = get_instance_launch_time(instance)
    now = datetime.datetime.utcnow()
    age = now - launch_time
    return age.total_seconds() / 3600 >= threshold_hours

if __name__ == "__main__":
    threshold_hours = 24

    log = []

    all_asg_names = get_asg_names()

    for asg_name in all_asg_names:
        instances_with_same_name = get_running_instances_by_asg_name(asg_name)
        asg_instances = get_asg_instances(asg_name)

        # Check if instances_with_same_name is empty (None)
        if instances_with_same_name is None:
            continue

        for instance in instances_with_same_name:
            instance_id = instance['InstanceId']
            instance_name = [tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'][0]

            if instance_id in asg_instances:
                continue  # Skip instances that are part of Auto Scaling Groups

            if is_instance_detached(instance_id):
                launch_time_str = instance['LaunchTime'].strftime("%Y-%m-%dT%H:%M:%S+00:00")
                launch_time = datetime.datetime.strptime(launch_time_str, "%Y-%m-%dT%H:%M:%S+00:00")
                if is_instance_old_enough(instance, threshold_hours):
                    log.append(f"Terminating instance {instance_id} (name: {instance_name}, launch time: {launch_time})")
                    # Uncomment the line below to actually terminate the instance
                    # terminate_instance(instance_id)
                else:
                    log.append(f"Skipping instance {instance_id} (name: {instance_name}, launch time: {launch_time})")

    # Print the log with all actions and skipped instances
    for entry in log:
        print(entry)
