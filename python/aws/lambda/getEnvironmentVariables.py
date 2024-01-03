import os
import json
import boto3

# Load data.json
with open('data.json', 'r') as file:
    data = json.load(file)

# 1. Get Lambda name
lambda_name = data['variables']['resources']['lambda'][0]['name']

# 2. Get environment info
env = os.getenv('env', 'default_env')  # Replace 'default_env' with your default environment

# 3. Construct new Lambda name
new_lambda_name = f"{lambda_name}-{env}-lbd"

# 4. Use boto3 to get environment variables of the AWS Lambda
lambda_client = boto3.client('lambda')
response = lambda_client.get_function_configuration(FunctionName=new_lambda_name)
lambda_env_variables = response['Environment']['Variables']

# 5. Update/merge the environment variables back into data.json
data['variables']['resources']['lambda'][0]['environmentVariables'] = lambda_env_variables

# Write the updated data back to data.json
with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)
