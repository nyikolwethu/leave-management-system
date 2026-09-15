import boto3
import json
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

dynamo = boto3.resource('dynamodb')
REQUESTS_TABLE = os.environ.get('LEAVE_REQUESTS_TABLE', 'LeaveRequests')
requests_table = dynamo.Table(REQUESTS_TABLE)

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

    claims = (event.get('requestContext', {}) or {}).get('authorizer', {}).get('claims', {}) or {}
    groups = claims.get('cognito:groups', '')
    requester_sub = claims.get('sub')
    if 'Managers' not in groups and requester_sub and requester_sub != employee_id:
        return response(403, {'error': 'Forbidden: cannot view another employee\'s history'})

    # requestId is the partition key and employeeId the sort key, so a Scan
    # with a filter is used here. For larger datasets, add a GSI on
    # employeeId to allow an efficient Query instead.
    items = []
    scan_kwargs = {'FilterExpression': Attr('employeeId').eq(employee_id)}
    while True:
        result = requests_table.scan(**scan_kwargs)
        items.extend(result.get('Items', []))
        if 'LastEvaluatedKey' not in result:
            break
        scan_kwargs['ExclusiveStartKey'] = result['LastEvaluatedKey']

    items.sort(key=lambda x: x.get('submittedAt', ''), reverse=True)

    return response(200, {'employeeId': employee_id, 'requests': items})
