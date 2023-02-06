import json
import requests
import boto3
from constants import c_list


def parse_json(raw_data):
    currency_list = raw_data['structure']['dimensions']['series'][1]['values']
    data = []

    for i, currency in enumerate(currency_list):
        key = f'0:{i}:0:0:0'
        observations = raw_data['dataSets'][0]['series'][key]['observations']
        total_observations = len(observations)

        current_day_key = str(total_observations - 1)
        previous_day_key = str(total_observations - 2)

        current_rate = observations[current_day_key][0]
        previous_day_rate = observations[previous_day_key][0]

        data.append({
            'currency': currency['id'],
            'current_rate': str(current_rate),
            'previous_day_rate': str(previous_day_rate)
        })

    return data


def store_exchange_rates(exchange_rates):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("ExchangeRates")

    for exchange_rate in exchange_rates:
        table.put_item(Item={
            "Currency": exchange_rate['currency'],
            "Rate": exchange_rate['current_rate'],
            "PreviousDayRate": exchange_rate['previous_day_rate'],
        })


def lambda_handler(event, context):
    # Here, '.' means all currencies
    param = [('dataflow', 'EXR'),
             ('freq', 'D'),
             ('currencies', '+'.join(c_list)),
             ('currency', 'EUR'),
             ('type', 'SP00'),
             ('series_variation', 'A'),
             ('start', '?startPeriod=2023-02-01')]
    params = '.'.join(value for key, value in param[1:-1])

    url = "https://sdw-wsrest.ecb.europa.eu/service/data/{}/{}{}".format(
        param[0][1], params, param[-1][1])
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the exchange rate data from the response
        exchange_rates = parse_json(response.json())

        # # Add logic to extract and store the exchange rates
        store_exchange_rates(exchange_rates)

        return {
            "statusCode": 200,
            "body": exchange_rates
        }
    else:
        return {
            "statusCode": response.status_code,
            "body": "Failed to fetch exchange rates"
        }
