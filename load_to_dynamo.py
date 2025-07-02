import boto3
import configparser
import time

def load(item):
    config = configparser.ConfigParser()
    config.read(r'C:\Users\mysur\OneDrive\Desktop\python_tutorial\venv1\config.config')

    aws_access_key_id = config['AWS']['aws_access_key_id']
    aws_secret_access_key = config['AWS']['aws_secret_access_key']
    region_name = config['AWS']['region']

    dynamodb = boto3.resource(
        'dynamodb',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    try:
        table = dynamodb.create_table(
            TableName='Tickets_data',
            KeySchema=[
                {
                    'AttributeName': '_id',
                    'KeyType': 'HASH'  
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': '_id',
                    'AttributeType': 'S'  
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        time.sleep(10)
        print("table created")
    except:
        print("table exist uploading to same...")

    tickets_table = dynamodb.Table('Tickets_data')
    with tickets_table.batch_writer() as batch:
        batch.put_item(Item=item)


def update_log(message, seq_token=None):

    LOG_GROUP = 'tickets-logs'
    LOG_STREAM = 'stream-1'

    config = configparser.ConfigParser()
    config.read(r'C:\Users\mysur\OneDrive\Desktop\python_tutorial\venv1\config.config')

    aws_access_key_id = config['AWS']['aws_access_key_id']
    aws_secret_access_key = config['AWS']['aws_secret_access_key']
    region_name = config['AWS']['region']

    client = boto3.client(
        'logs',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    try:
        client.create_log_group(logGroupName=LOG_GROUP)
    except:
        pass

    try:
        client.create_log_stream(
            logGroupName=LOG_GROUP,
            logStreamName=LOG_STREAM
        )
    except:
        pass

    timestamp = int(time.time() * 1000)

    args = {
        'logGroupName': LOG_GROUP,
        'logStreamName': LOG_STREAM,
        'logEvents': [
            {'timestamp': timestamp, 'message': message}
        ]
    }

    if seq_token:
        args['sequenceToken'] = seq_token

    response = client.put_log_events(**args)

    return response['nextSequenceToken']
