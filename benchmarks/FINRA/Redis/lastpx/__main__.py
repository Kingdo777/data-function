import json
import pickle
import time
import redis


def timestamp(response, event, execute_start_time, execute_end_time, transport_start_time, transport_end_time):
    stamp_begin = 1000 * time.time()
    prior_execute_time = event['executeTime'] if 'executeTime' in event else 0
    response['executeTime'] = prior_execute_time + execute_end_time - execute_start_time

    prior_interaction_time = event['interactionTime'] if 'interactionTime' in event else 0
    response['interactionTime'] = prior_interaction_time + transport_end_time - transport_start_time

    prior_cost = event['timeStampCost'] if 'timeStampCost' in event else 0
    response['timeStampCost'] = prior_cost - (stamp_begin - 1000 * time.time())
    return response


def main(event):
    startTime = 1000 * time.time()

    index = event['index']
    portfolio = event['body']['portfolio']
    portfolios = json.loads(open('data/portfolios.json', 'r').read())
    data = portfolios[portfolio]

    valid = True

    for trade in data:
        px = str(trade['LastPx'])
        if '.' in px:
            a, b = px.split('.')
            if not ((len(a) == 3 and len(b) == 6) or
                    (len(a) == 4 and len(b) == 5) or
                    (len(a) == 5 and len(b) == 4) or
                    (len(a) == 6 and len(b) == 3)):
                print('{}: {}v{}'.format(px, len(a), len(b)))
                valid = False
                break
    redis_client = redis.Redis(host='222.20.94.67', port=6379, db=0)
    body_data = pickle.dumps({'valid': valid, 'portfolio': portfolio})
    response = {'statusCode': 200}
    endTime = 1000 * time.time()

    transport_start_time = endTime
    redis_client.set("lastpx_body_{}".format(index), body_data)
    transport_end_time = 1000 * time.time()

    return timestamp(response, event, startTime, endTime, transport_start_time, transport_end_time)


if __name__ == "__main__":
    print(main({"body": {"portfolio": "1234"}}))
