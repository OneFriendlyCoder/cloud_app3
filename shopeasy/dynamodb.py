import os
import boto3
import botocore.exceptions
from botocore.exceptions import ClientError

def get_dynamodb_resource():
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    return boto3.resource("dynamodb", region_name=region)

def get_cart_table():
    dynamodb = get_dynamodb_resource()
    table_name = os.environ.get("DYNAMODB_CART_TABLE", "ShopeasyCart")
    return dynamodb.Table(table_name)

def get_counters_table():
    dynamodb = get_dynamodb_resource()
    table_name = os.environ.get("DYNAMODB_COUNTERS_TABLE", "ShopeasyCounters")
    return dynamodb.Table(table_name)

def get_cart(user_id):
    table = get_cart_table()
    try:
        response = table.get_item(Key={"user_id": user_id})
        return response.get("Item", {"user_id": user_id, "items": []})
    except (ClientError, botocore.exceptions.BotoCoreError) as e:
        print(f"Error fetching cart: {e}")
        return {"user_id": user_id, "items": []}

def update_cart(user_id, items):
    import time
    table = get_cart_table()
    try:
        # Task 4.7: Configure TTL (24 hours = 86400 seconds)
        ttl_value = int(time.time()) + 86400
        table.put_item(Item={
            "user_id": user_id, 
            "items": items,
            "expires_at": ttl_value
        })
    except (ClientError, botocore.exceptions.BotoCoreError) as e:
        print(f"Error updating cart: {e}")

def increment_product_view(product_id):
    table = get_counters_table()
    try:
        response = table.update_item(
            Key={"product_id": str(product_id)},
            UpdateExpression="ADD view_count :inc",
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW"
        )
        return response.get("Attributes", {}).get("view_count", 1)
    except (ClientError, botocore.exceptions.BotoCoreError) as e:
        print(f"Error incrementing view: {e}")
        return 0

def get_product_view(product_id):
    table = get_counters_table()
    try:
        response = table.get_item(Key={"product_id": str(product_id)})
        return response.get("Item", {}).get("view_count", 0)
    except (ClientError, botocore.exceptions.BotoCoreError) as e:
        return 0
