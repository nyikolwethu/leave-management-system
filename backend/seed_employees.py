"""
Seeds the leave-mgmt-Employees table using the users that already
exist in Cognito (Managers and Employees groups).
Run from the backend folder:  python seed_employees.py
"""
import boto3

REGION = 'us-east-1'
STACK_NAME = 'leave-mgmt'

cf = boto3.client('cloudformation', region_name=REGION)
cognito = boto3.client('cognito-idp', region_name=REGION)
dynamo = boto3.resource('dynamodb', region_name=REGION)

# Find the user pool created by the stack
outputs = cf.describe_stacks(StackName=STACK_NAME)['Stacks'][0]['Outputs']
pool_id = next(o['OutputValue'] for o in outputs if o['OutputKey'] == 'UserPoolId')


def users_in_group(group):
    resp = cognito.list_users_in_group(UserPoolId=pool_id, GroupName=group)
    found = []
    for user in resp['Users']:
        attrs = {a['Name']: a['Value'] for a in user['Attributes']}
        found.append({'sub': attrs['sub'], 'email': attrs['email']})
    return found


managers = users_in_group('Managers')
employees = users_in_group('Employees')

if not managers or not employees:
    raise SystemExit('Need at least one user in Managers and one in Employees.')

table = dynamo.Table('leave-mgmt-Employees')
manager_sub = managers[0]['sub']

for m in managers:
    table.put_item(Item={
        'employeeId': m['sub'],
        'name': 'Manager',
        'email': m['email'],
        'role': 'MANAGER',
        'leaveBalance': {'annual': 20, 'sick': 10, 'unpaid': 30}
    })
    print(f"Seeded manager  {m['email']}")

for e in employees:
    table.put_item(Item={
        'employeeId': e['sub'],
        'name': 'Employee',
        'email': e['email'],
        'managerId': manager_sub,
        'role': 'EMPLOYEE',
        'leaveBalance': {'annual': 15, 'sick': 10, 'unpaid': 30}
    })
    print(f"Seeded employee {e['email']}")