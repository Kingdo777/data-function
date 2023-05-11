import json
from utils import *


def checkMarginBalance(portfolioData, marketData, portfolio):
    marginAccountBalance = json.loads(open('data/marginBalance.json', 'r').read())[portfolio]

    portfolioMarketValue = 0
    for trade in portfolioData:
        security = trade['Security']
        qty = trade['LastQty']
        portfolioMarketValue += qty * marketData[security]

    # Maintenance Margin should be atleast 25% of market value for "long" securities
    # https://www.finra.org/rules-guidance/rulebooks/finra-rules/4210#the-rule
    result = False
    if marginAccountBalance >= 0.25 * portfolioMarketValue:
        result = True

    return result


def main(events):
    startTime = 1000 * time.time()
    marketData = {}
    validFormat = True
    portfolio = ""

    for event in events:
        body = event['body']
        if 'marketData' in body:
            marketData = body['marketData']
        elif 'valid' in body:
            portfolio = event['body']['portfolio']
            validFormat = validFormat and body['valid']

    portfolios = json.loads(open('data/portfolios.json', 'r').read())
    portfolioData = portfolios[portfolio]
    marginSatisfied = checkMarginBalance(portfolioData, marketData, portfolio)

    response = {'statusCode': 200,
                'body': {'validFormat': validFormat, 'marginSatisfied': marginSatisfied}}

    endTime = 1000 * time.time()

    time_statistics = agg_timestamp({}, events, startTime, endTime)
    response["workflowAllTime"] = "{:.2f} ms".format(
        time_statistics["workflowEndTime"] - time_statistics["workflowStartTime"])
    response["executeTime"] = "{:.2f} ms".format(time_statistics["duration"])
    response["timeStampCost"] = "{:.2f} ms".format(time_statistics["timeStampCost"])
    response["interactionTime"] = "{:.2f} ms".format(
        time_statistics["workflowEndTime"] - time_statistics["workflowStartTime"] -
        time_statistics["duration"] -
        time_statistics["timeStampCost"])

    return response
