import boto3
import json
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

dynamo = boto3.resource('dynamodb')
REQUESTS_TABLE = os.environ.get('LEAVE_REQUESTS_TABLE', 'LeaveRequests')
EMPLOYEES_TABLE = os.environ.get('EMPLOYEES_TABLE', 'Employees')
requests_table = dynamo.Table(REQUESTS_TABLE)
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


def scan_all(table, **kwargs):
    items = []
    while True:
        result = table.scan(**kwargs)
        items.extend(result.get('Items', []))
        if 'LastEvaluatedKey' not in result:
            break
        kwargs['ExclusiveStartKey'] = result['LastEvaluatedKey']
    return items


def lambda_handler(event, context):
    manager_id = (event.get('pathParameters') or {}).get('id')
    if not manager_id:
        return response(400, {'error': 'Missing manager id in path'})

    claims = (event.get('requestContext', {}) or {}).get('authorizer', {}).get('claims', {}) or {}
    groups = claims.get('cognito:groups', '')
    if 'Managers' not in groups:
        return response(403, {'error': 'Forbidden: manager role required'})

    # Find direct reports of this manager (small team sizes, so a scan+filter is fine;
    # for larger orgs add a GSI on managerId to Employees).
    reports = scan_all(employees_table, FilterExpression=Attr('managerId').eq(manager_id))
    report_ids = {emp['employeeId'] for emp in reports}
    if not report_ids:
        return response(200, {'managerId': manager_id, 'pendingRequests': []})

    # Pull all PENDING requests, then keep only those belonging to direct reports.
    # For larger datasets, add a GSI on `status` to query PENDING directly.
    pending = scan_all(requests_table, FilterExpression=Attr('status').eq('PENDING'))
    pending = [r for r in pending if r.get('employeeId') in report_ids]
    pending.sort(key=lambda x: x.get('submittedAt', ''))

    return response(200, {'managerId': manager_id, 'pendingRequests': pending})
