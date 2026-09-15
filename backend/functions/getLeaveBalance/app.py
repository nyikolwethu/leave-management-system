import boto3
import json
import os
from decimal import Decimal

dynamo = boto3.resource('dynamodb')
EMPLOYEES_TABLE = os.environ.get('EMPLOYEES_TABLE', 'Employees')
employees_table = dynamo.Table(EMPLOYEES_TABLE)

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'OPTIONS,GET'
}


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)


def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': CORS_HEADERS,
        'body': json.dumps(body, cls=DecimalEncoder)
    }


def lambda_handler(event, context):
    employee_id = (event.get('pathParameters') or {}).get('id')
    if not employee_id:
        return response(400, {'error': 'Missing employee id in path'})

    # Optional: restrict employees to viewing only their own balance
    claims = (event.get('requestContext', {}) or {}).get('authorizer', {}).get('claims', {}) or {}
    groups = claims.get('cognito:groups', '')
    requester_sub = claims.get('sub')
    if 'Managers' not in groups and requester_sub and requester_sub != employee_id:
        return response(403, {'error': 'Forbidden: cannot view another employee\'s balance'})

    item = employees_table.get_item(Key={'employeeId': employee_id}).get('Item')
    if not item:
        return response(404, {'error': f'Employee {employee_id} not found'})

    return response(200, {
        'employeeId': employee_id,
        'name': item.get('name'),
        'leaveBalance': item.get('leaveBalance', {})
    })
