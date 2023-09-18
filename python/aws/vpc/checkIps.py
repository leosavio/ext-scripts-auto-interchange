import boto3
import ipaddress

ec2 = boto3.client('ec2')

# Get list of VPC IDs
response = ec2.describe_vpcs() 
vpc_ids = [vpc['VpcId'] for vpc in response['Vpcs']]

for vpc_id in vpc_ids:

  # Get VPC CIDR
  response = ec2.describe_vpcs(VpcIds=[vpc_id])
  vpc_cidr = response['Vpcs'][0]['CidrBlock']  

  # Calculate total IPs
  ip_network = ipaddress.ip_network(vpc_cidr)
  total_ips = ip_network.num_addresses

  # Get interfaces and in-use IPs
  response = ec2.describe_network_interfaces(
      Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
  )
  in_use_ips = [eni['PrivateIpAddress'] for eni in response['NetworkInterfaces']]
  num_in_use = len(in_use_ips)

  # Print results
  print(f"VPC {vpc_id}")
  print(f"CIDR: {vpc_cidr}")
  print(f"Total IPs: {total_ips}") 
  print(f"IPs in use: {num_in_use}")
