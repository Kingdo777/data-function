import json
from utils import *


def main(event):
    startTime = 1000 * time.time()

    portfolio = event['body']['portfolio']
    portfolios = json.loads(open('data/portfolios.json', 'r').read())
    data = portfolios[portfolio]

    valid = True

    for trade in data:
        qty = str(trade['LastQty'])
        # Tag ID: 32, Tag Name: LastQty, Format: max 8 characters, no decimal
        if (len(qty) > 8) or ('.' in qty):
            valid = False
            break

    response = {'statusCode': 200, 'body': {'valid': valid, 'portfolio': portfolio}}
    print(response)
    endTime = 1000 * time.time()
    return timestamp(response, event, startTime, endTime)


if __name__ == "__main__":
    print(main({"body": {"portfolio": "1234"}}))
