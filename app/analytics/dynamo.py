#Reads views, interest counts, and trends from DynamoDB
import os
import boto3
from boto3.dynamodb.conditions import Key

def get_property_analytics(property_ids: list) -> str:
    """
    Fetches analytics (views and interests) from DynamoDB for the given property IDs.
    """
    if not property_ids:
        return "No analytics available for these properties."

    try:
        dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )
        view_table = dynamodb.Table("PropertyViewEvents")
        interest_table = dynamodb.Table("PropertyInterestEvents")
        
        analytics_summary = []
        
        for pid in property_ids:
            pid_str = str(pid)
            
            # 1. Fetch Views
            view_response = view_table.query(
                KeyConditionExpression=Key("property_id").eq(pid_str)
            )
            total_views = sum(int(item.get("view_count", 0)) for item in view_response.get("Items", []))
            
            # 2. Fetch Interests
            interest_response = interest_table.query(
                KeyConditionExpression=Key("property_id").eq(pid_str)
            )
            total_interests = len(interest_response.get("Items", []))
            
            if total_views > 0 or total_interests > 0:
                summary = f"Property ID {pid_str}: {total_views} views and {total_interests} interest signals recorded."
                analytics_summary.append(summary)
        
        if not analytics_summary:
            return "Minimal market traffic data for these properties currently."
            
        return "\n".join(analytics_summary)

    except Exception as e:
        print(f"Error fetching analytics: {e}")
        return "Analytics service temporarily unavailable."

