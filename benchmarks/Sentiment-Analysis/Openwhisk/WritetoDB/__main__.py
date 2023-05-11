import boto3
import time


def timestamp(response, event, execute_start_time, execute_end_time, transport_start_time, transport_end_time):
    stamp_begin = 1000 * time.time()
    prior_execute_time = event['executeTime'] if 'executeTime' in event else 0
    response['executeTime'] = prior_execute_time + execute_end_time - execute_start_time

    print(transport_end_time - transport_start_time)

    prior_interaction_time = event['interactionTime'] if 'interactionTime' in event else 0
    response['interactionTime'] = prior_interaction_time + transport_end_time - transport_start_time

    prior_cost = event['timeStampCost'] if 'timeStampCost' in event else 0
    response['timeStampCost'] = prior_cost - (stamp_begin - 1000 * time.time())

    return response


def main(event):
    body_sentiment = event["body_sentiment"]

    startTime = 1000 * time.time()

    dynamodb = boto3.client('dynamodb', aws_access_key_id="AKIAQ4WHHPCKGVH4HO6S",
                            aws_secret_access_key="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",
                            region_name="us-east-1")

    # select correct table based on input data
    if body_sentiment['reviewType'] == 0:
        tableName = 'faastlane-products-table'
    elif body_sentiment['reviewType'] == 1:
        tableName = 'faastlane-services-table'
    else:
        raise Exception("Input review is neither Product nor Service")

    # Not publishing to table to avoid network delays in experiments

    endTime = 1000 * time.time()

    response = {
        'statusCode': 200,
        'body_sentiment': body_sentiment,
        "transport_start_time": endTime
    }
    response["end"] = 1000 * time.time()
    print(endTime-startTime)

    return timestamp(response, event, startTime, endTime, event['transport_start_time'], startTime)


if __name__ == "__main__":
    print(main({'statusCode': 200,
                'body_sentiment': {
                    'sentiment': 1,
                    'reviewType': 0,
                    'reviewID': '123',
                    'customerID': '456',
                    'productID': '789',
                    'feedback': 'Great product'},
                'transport_start_time': 1683460303476.641,
                'executeTime': 312.311279296875,
                'interactionTime': 62494.548828125,
                'timeStampCost': 0.005859375}
               ))
