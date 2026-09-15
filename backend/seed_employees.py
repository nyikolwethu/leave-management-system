"""
One-off script to seed the Employees table with sample data for testing.
Run locally with AWS credentials configured:
    pip install boto3
    python seed_employees.py
"""
import boto3

dynamo = boto3.resource('dynamodb')
table = dynamo.Table('Employees')

sample_employees = [
    {
        'employeeId': 'EMP-0001',
        'name': 'Alex Manager',
        'email': 'alex.manager@example.com',
        'managerId': None,
        'role': 'MANAGER',
        'leaveBalance': {'annual': 20, 'sick': 10, 'unpaid': 30}
    },
    {
        'employeeId': 'EMP-0042',
        'name': 'Jamie Employee',
        'email': 'jamie.employee@example.com',
        'managerId': 'EMP-0001',
        'role': 'EMPLOYEE',
        'leaveBalance': {'annual': 15, 'sick': 10, 'unpaid': 30}
    }
]

for emp in sample_employees:
    table.put_item(Item=emp)
    print(f"Seeded {emp['employeeId']} ({emp['name']})")
