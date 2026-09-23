import boto3
import json
import os
from datetime import datetime
from decimal import Decimal

dynamo = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

REQUESTS_TABLE = os.environ.get('LEAVE_REQUESTS_TABLE', 'LeaveRequests')
EMPLOYEES_TABLE = os.environ.get('EMPLOYEES_TABLE', 'Employees')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'leave-system@yourcompany.com')

requests_table = dynamo.Table(REQUESTS_TABLE)
employees_table = dynamo.Table(EMPLOYEES_TABLE)

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'OPTIONS,PUT'
}


def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': CORS_HEADERS,
        'body': json.dumps(body)
    }


def lambda_handler(event, context):
    # Enforce that only Managers can approve/reject (Cognito group claim)
    claims = (event.get('requestContext', {}) or {}).get('authorizer', {}).get('claims', {}) or {}
    groups = claims.get('cognito:groups', '')
    if 'Managers' not in groups:
        return response(403, {'error': 'Forbidden: manager role required'})

    request_id = (event.get('pathParameters') or {}).get('requestId')
    if not request_id:
        return response(400, {'error': 'Missing requestId in path'})

    try:
        body = json.loads(event.get('body') or '{}')
    except json.JSONDecodeError:
        return response(400, {'error': 'Invalid JSON body'})

    new_status = (body.get('status') or '').upper()
    if new_status not in ('APPROVED', 'REJECTED'):
        return response(400, {'error': 'status must be APPROVED or REJECTED'})

    approver_id = claims.get('sub') or body.get('approverId')
    if not approver_id:
        return response(400, {'error': 'Could not determine approverId'})

    # We need employeeId (the sort key) to fetch/update the item; require it in body
    employee_id = body.get('employeeId')
    if not employee_id:
        return response(400, {'error': 'Missing employeeId in body'})

    existing = requests_table.get_item(
        Key={'requestId': request_id, 'employeeId': employee_id}
    ).get('Item')

    if not existing:
        return response(404, {'error': 'Leave request not found'})

    if existing['status'] != 'PENDING':
        return response(409, {'error': f'Request already {existing["status"]}, cannot modify'})

    updated = requests_table.update_item(
        Key={'requestId': request_id, 'employeeId': employee_id},
        UpdateExpression='SET #s = :status, approverId = :approver, decidedAt = :decidedAt',
        ExpressionAttributeNames={'#s': 'status'},
        ExpressionAttributeValues={
            ':status': new_status,
            ':approver': approver_id,
            ':decidedAt': datetime.utcnow().isoformat() + 'Z'
        },
        ReturnValues='ALL_NEW'
    )['Attributes']

    # If approved, deduct from the employee's leave balance
    if new_status == 'APPROVED' and existing['leaveType'] != 'UNPAID':
        balance_key = existing['leaveType'].lower()
        num_days = existing.get('numDays', Decimal('0'))
        try:
            employees_table.update_item(
                Key={'employeeId': employee_id},
                UpdateExpression=f'SET leaveBalance.#b = leaveBalance.#b - :d',
                ExpressionAttributeNames={'#b': balance_key},
                ExpressionAttributeValues={':d': num_days}
            )
        except Exception as e:
            print(f'Failed to update leave balance: {e}')

    # Notify the employee of the decision
    emp = employees_table.get_item(Key={'employeeId': employee_id}).get('Item')
    if emp and emp.get('email'):
        try:
            send_email(
                emp['email'],
                f'Your leave request has been {new_status.lower()}',
                f'''<p>Your {existing["leaveType"].lower()} leave request from
                {existing["startDate"]} to {existing["endDate"]} has been
                <strong>{new_status.lower()}</strong>.</p>'''
            )
        except Exception as e:
            print(f'Failed to send notification email: {e}')

    return response(200, updated)


def send_email(to_email, subject, body_html):
    ses.send_email(
        Source=SENDER_EMAIL,
        Destination={'ToAddresses': [to_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Html': {'Data': body_html}}
        }
    )
