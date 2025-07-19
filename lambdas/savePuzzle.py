#!/usr/bin/env python3
"""
Backend script to save puzzles to DynamoDB.
Receives puzzle data from frontend and stores it in DynamoDB tables.
"""

import json
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    """
    AWS Lambda handler function for saving puzzles.
    
    Args:
        event: Contains the puzzle data in the body
        context: Lambda context (unused)
    
    Returns:
        HTTP response with status and message
    """
    
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    settings_table = dynamodb.Table('Settings')
    puzzles_table = dynamodb.Table('Puzzles')
    
    try:
        # Parse the request body to get the puzzle
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
            
        puzzle = body.get('puzzle')
        
        if not puzzle:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'No puzzle data provided'})
            }
        
        # Get the current puzzle count from Settings table
        response = settings_table.get_item(
            Key={'settingName': 'numPuzzles'}
        )
        
        if 'Item' not in response:
            # Initialize if not exists
            raise Exception("numPuzzles not found in settings table")
        else:
            current_count = int(response['Item']['value'])
        
        # Use the current count as the puzzle ID
        puzzle_id = current_count
        
        # Save the puzzle to Puzzles table
        puzzles_table.put_item(
            Item={
                'puzzleId': puzzle_id,
                'puzzle': puzzle,
                'humanGenerated': True
            }
        )
        
        # Update the puzzle count in Settings
        settings_table.update_item(
            Key={'settingName': 'numPuzzles'},
            UpdateExpression='SET #v = :val',
            ExpressionAttributeNames={'#v': 'value'},
            ExpressionAttributeValues={':val': current_count + 1}
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Puzzle saved successfully',
                'puzzleId': puzzle_id
            })
        }
        
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Database error: {str(e)}'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Server error: {str(e)}'
            })
        }


def main():
    """
    Main function for local testing.
    """
    # Example test event
    test_event = {
        'body': json.dumps({
            'puzzle': 'Test puzzle data here'
        })
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()