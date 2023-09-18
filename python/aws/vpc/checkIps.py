import boto3

ec2 = boto3.client('ec2')

# Get list of VPC IDs 
response = ec2.describe_vpcs()
vpc_ids = [vpc['VpcId'] for vpc in response['Vpcs']]

for vpc_id in vpc_ids:

  # Get VPC info
  response = ec2.describe_vpcs(VpcIds=[vpc_id])
  
  vpc_cidr = response['Vpcs'][0]['CidrBlock']
  avail_ips = response['Vpcs'][0]['AvailableIpAddressCount']

  print(f"VPC {vpc_id} CIDR: {vpc_cidr}")
  print(f"Available IPs: {avail_ips}")
  
  # Get in-use IPs
  response = ec2.describe_network_interfaces(
      Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
  )

  ip_addresses = [eni['PrivateIpAddress'] for eni in response['NetworkInterfaces']]

  print(f"IPs in use in {vpc_id}:")
  for ip in ip_addresses:
    print(ip)

  print() # newline between VPCs
