import boto3
import os
import urllib.parse
import uuid
from datetime import datetime

print('Loading function')

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    
    # 1. Get bucket and key from S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        # 2. Get object metadata
        response = s3.head_object(Bucket=bucket, Key=key)
        file_size = response['ContentLength']
        content_type = response['ContentType']
        etag = response['ETag'].strip('"')
        
        # 3. Prepare item for DynamoDB
        item_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        item = {
            'id': item_id,
            'file_key': key,
            'bucket': bucket,
            'file_size_bytes': file_size,
            'content_type': content_type,
            'etag': etag,
            'processed_at': timestamp
        }
        
        # 4. Write to DynamoDB
        table.put_item(Item=item)
        
        print(f"SUCCESS: Processed {key} from {bucket}. Registered in DynamoDB with id {item_id}.")
        
        return {
            'statusCode': 200,
            'body': f"File {key} processed successfully."
        }

    except Exception as e:
        print(f"ERROR: Failed to process {key} from {bucket}.")
        print(str(e))
        raise e
