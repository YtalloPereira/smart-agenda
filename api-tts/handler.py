import json
import hashlib
import boto3
from datetime import datetime

bucket_name = "audios-polly-ytallo"
dynamo_table_name = "audios"

polly_client = boto3.client('polly')
s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')


def health(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def v1_description(event, context):
    body = {
        "message": "TTS api version 1."
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

def generate_audio_from_text(event, context):
    request_body = json.loads(event['body'])
    phrase = request_body.get('phrase', '')

    if not phrase:
        return {"statusCode": 400, "body": json.dumps({"error": "Phrase is required"})}

    hash_object = hashlib.md5(phrase.encode())
    unique_id = hash_object.hexdigest()

    try:
        dynamo_response = dynamodb_client.get_item(
            TableName=dynamo_table_name,
            Key={'unique_id': {'S': unique_id}}
        )
        if 'Item' in dynamo_response:
            url_to_audio = dynamo_response['Item']['url_to_audio']['S']
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "received_phrase": phrase,
                    "url_to_audio": url_to_audio,
                    "created_audio": dynamo_response['Item']['created_audio']['S'],
                    "unique_id": unique_id
                })
            }
    except Exception as e:
        print(f"Erro ao consultar DynamoDB: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": "Erro ao consultar DynamoDB"})}
    
    try:
        response = polly_client.synthesize_speech(
            Text=phrase,
            OutputFormat='mp3',
            VoiceId='Ricardo',
            Engine='standard'
        )
        
        audio_key = f"{unique_id}.mp3"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=audio_key,
            Body=response['AudioStream'].read(),
            ContentType='audio/mpeg'
        )
        
        dynamodb_client.put_item(
            TableName=dynamo_table_name,
            Item={
                'unique_id': {'S': unique_id},
                'url_to_audio': {'S': f"https://{bucket_name}.s3.amazonaws.com/{audio_key}"},
                'created_audio': {'S': datetime.now().isoformat()}
            }
        )

        url_to_audio = f"https://{bucket_name}.s3.amazonaws.com/{audio_key}"

    except Exception as e:
        print(f"Erro ao gerar áudio ou salvar no S3: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": "Erro ao gerar áudio ou salvar no S3"})}

    body = {
        "received_phrase": phrase,
        "url_to_audio": url_to_audio,
        "created_audio": datetime.now().isoformat(),
        "unique_id": unique_id
    }

    return {"statusCode": 200, "body": json.dumps(body)}