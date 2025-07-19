#!/usr/bin/env python3
"""
Backend script to retrieve puzzles from DynamoDB.
Receives a puzzle ID and returns the corresponding puzzle data.
"""

import json
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    """
    AWS Lambda handler function for retrieving puzzles.
    
    Args:
        event: Contains the puzzle ID as a query parameter
        context: Lambda context (unused)
    
    Returns:
        HTTP response with puzzle data or error message
    """
    
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    puzzles_table = dynamodb.Table('Puzzles')
    
    try:
        # Extract puzzle ID from query string parameters only
        puzzle_id = None
        
        if 'queryStringParameters' in event and event['queryStringParameters']:
            puzzle_id = event['queryStringParameters'].get('puzzleId')
        
        if puzzle_id is None:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'No puzzle ID provided'})
            }
        
        # Convert puzzle_id to integer
        try:
            puzzle_id = int(puzzle_id)
        except ValueError:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Invalid puzzle ID format'})
            }
        
        # Retrieve the puzzle from DynamoDB
        response = puzzles_table.get_item(
            Key={'puzzleId': puzzle_id}
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': f'Puzzle with ID {puzzle_id} not found'})
            }
        
        # Extract and return only the puzzle data
        puzzle_data = response['Item']['puzzle']
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': puzzle_data  # Already JSON, return as-is
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
    # Example test events
    test_events = [
        # Test with valid puzzle ID
        {
            'queryStringParameters': {'puzzleId': '1'}
        },
        # Test with different puzzle ID
        {
            'queryStringParameters': {'puzzleId': '2'}
        },
        # Test with missing query parameters
        {},
        # Test with missing puzzleId parameter
        {
            'queryStringParameters': {'someOtherParam': 'value'}
        },
        # Test with invalid puzzle ID
        {
            'queryStringParameters': {'puzzleId': 'invalid'}
        }
    ]
    
    for i, test_event in enumerate(test_events):
        print(f"\nTest {i + 1}:")
        print(f"Event: {test_event}")
        result = lambda_handler(test_event, None)
        print(f"Result: {json.dumps(result, indent=2)}")


if __name__ == '__main__':
    main()