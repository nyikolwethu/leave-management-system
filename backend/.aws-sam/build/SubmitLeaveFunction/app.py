import boto3
import json
import uuid
import os
from datetime import datetime, date
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
    'Access-Control-Allow-Methods': 'OPTIONS,POST'
}

VALID_LEAVE_TYPES = {'ANNUAL', 'SICK', 'UNPAID'}


def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': CORS_HEADERS,
        'body': json.dumps(body)
    }


def business_days(start_str, end_str):
    start = date.fromisoformat(start_str)
    end = date.fromisoformat(end_str)
    if end < start:
        return -1
    days = 0
    current = start
    while current <= end:
        if current.weekday() < 5:  # Mon-Fri
            days += 1
        current += __import__('datetime').timedelta(days=1)
    return days


def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body') or '{}')
    except json.JSONDecodeError:
        return response(400, {'error': 'Invalid JSON body'})

    required_fields = ['employeeId', 'leaveType', 'startDate', 'endDate']
    missing = [f for f in required_fields if not body.get(f)]
    if missing:
        return response(400, {'error': f'Missing required fields: {", ".join(missing)}'})

    leave_type = body['leaveType'].upper()
    if leave_type not in VALID_LEAVE_TYPES:
        return response(400, {'error': f'leaveType must be one of {sorted(VALID_LEAVE_TYPES)}'})

    try:
        num_days = business_days(body['startDate'], body['endDate'])
    except ValueError:
        return response(400, {'error': 'Dates must be ISO 8601 format, e.g. 2025-08-01'})

    if num_days <= 0:
        return response(400, {'error': 'endDate must be on or after startDate'})

    # Look up employee to validate existence and check balance
    emp_resp = employees_table.get_item(Key={'employeeId': body['employeeId']})
    employee = emp_resp.get('Item')
    if not employee:
        return response(404, {'error': f'Employee {body["employeeId"]} not found'})

    balance_key = leave_type.lower()
    current_balance = employee.get('leaveBalance', {}).get(balance_key, 0)
    if leave_type != 'UNPAID' and Decimal(str(num_days)) > Decimal(str(current_balance)):
        return response(400, {
            'error': f'Insufficient {balance_key} balance: requested {num_days}, available {current_balance}'
        })

    item = {
        'requestId': f'req-{uuid.uuid4()}',
        'employeeId': body['employeeId'],
        'leaveType': leave_type,
        'startDate': body['startDate'],
        'endDate': body['endDate'],
        'status': 'PENDING',
        'reason': body.get('reason', ''),
        'submittedAt': datetime.utcnow().isoformat() + 'Z',
        'numDays': Decimal(str(num_days))
    }

    requests_table.put_item(Item=item)

    # Notify the manager, if one is set and their email is on file
    manager_id = employee.get('managerId')
    if manager_id:
        mgr_resp = employees_table.get_item(Key={'employeeId': manager_id})
        manager = mgr_resp.get('Item')
        if manager and manager.get('email'):
            try:
                send_email(
                    manager['email'],
                    f'New leave request from {employee.get("name", body["employeeId"])}',
                    f'''<p>{employee.get("name", body["employeeId"])} has submitted a
                    {leave_type.lower()} leave request from {body["startDate"]} to
                    {body["endDate"]} ({num_days} business day(s)).</p>
                    <p>Reason: {body.get("reason", "N/A")}</p>
                    <p>Request ID: {item["requestId"]}</p>'''
                )
            except Exception as e:
                # Don't fail the request just because the email didn't send
                print(f'Failed to send notification email: {e}')

    return response(201, {
        'requestId': item['requestId'],
        'status': item['status'],
        'numDays': num_days
    })


def send_email(to_email, subject, body_html):
    ses.send_email(
        Source=SENDER_EMAIL,
        Destination={'ToAddresses': [to_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Html': {'Data': body_html}}
        }
    )
