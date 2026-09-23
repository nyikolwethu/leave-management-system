import boto3
import os

dynamo = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

EMPLOYEES_TABLE = os.environ.get('EMPLOYEES_TABLE', 'Employees')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'leave-system@yourcompany.com')
LOW_BALANCE_THRESHOLD = 2

employees_table = dynamo.Table(EMPLOYEES_TABLE)


def lambda_handler(event, context):
    """Triggered on a schedule (e.g. weekly via EventBridge) to warn
    employees whose annual leave balance is running low."""
    notified = 0
    scan_kwargs = {}
    while True:
        result = employees_table.scan(**scan_kwargs)
        for emp in result.get('Items', []):
            balance = emp.get('leaveBalance', {}).get('annual', 0)
            if balance < LOW_BALANCE_THRESHOLD and emp.get('email'):
                try:
                    ses.send_email(
                        Source=SENDER_EMAIL,
                        Destination={'ToAddresses': [emp['email']]},
                        Message={
                            'Subject': {'Data': 'Your annual leave balance is low'},
                            'Body': {'Html': {'Data': (
                                f'<p>Hi {emp.get("name", "")}, you have '
                                f'{balance} annual leave day(s) remaining.</p>'
                            )}}
                        }
                    )
                    notified += 1
                except Exception as e:
                    print(f'Failed to notify {emp.get("employeeId")}: {e}')
        if 'LastEvaluatedKey' not in result:
            break
        scan_kwargs['ExclusiveStartKey'] = result['LastEvaluatedKey']

    return {'notified': notified}
