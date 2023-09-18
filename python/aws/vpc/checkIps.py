import boto3
import ipaddress

ec2 = boto3.client('ec2')

# Get VPC IDs
response = ec2.describe_vpcs()
vpc_ids = [vpc['VpcId'] for vpc in response['Vpcs']]

for vpc_id in vpc_ids:

  # Get VPC CIDR
  response = ec2.describe_vpcs(VpcIds=[vpc_id])
  vpc_cidr = response['Vpcs'][0]['CidrBlock']

  # Calculate total IPs
  ip_network = ipaddress.ip_network(vpc_cidr)
  total_ips = ip_network.num_addresses  

  # Get subnets
  response = ec2.describe_subnets(
      Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
  )

  print(f"VPC {vpc_id}")
  
  # Print subnets
  print("Subnets:")
  for subnet in response['Subnets']:
    print(f"- {subnet['SubnetId']} ({subnet['CidrBlock']})")

  # Get interfaces
  response = ec2.describe_network_interfaces(
      Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
  )

  # Initialize counter 
  num_in_use = 0

  # Loop through interfaces
  for eni in response['NetworkInterfaces']:

    # Count secondary IPs
    secondary_ips = eni['PrivateIpAddresses'][1:]
    num_in_use += len(secondary_ips)

  # Print results
  print(f"Total IPs: {total_ips}")
  print(f"IPs in use: {num_in_use}")
  
  print() # newline between VPCs
