import requests
import sys

url = 'https://j8fnoktyyb.execute-api.ap-northeast-1.amazonaws.com/prod/exchange-rate'


def calculate_percentage_change(old_value, new_value):
    # Try to convert the values to float, or exit if they are not valid numbers
    try:
        old_value = float(old_value)
        new_value = float(new_value)
    except ValueError:
        print("Error: old_value and new_value must be numbers.")
        sys.exit(1)

    # Calculate the percentage change using the formula
    percentage_change = ((new_value - old_value) / old_value) * 100

    # Return the percentage change
    return percentage_change


"""
The function get_exchange_rate_againts_EUR takes two arguments:

currency (str): The currency for which the exchange rate is to be retrieved from the API.

show_change (bool, optional): This argument determines whether to show the percentage change from the previous day's rate or not. The default value is False.

The function first retrieves the exchange rate data from the API using the requests library. If the response status code is 200, then it filters the exchange rates data to get the rate for the provided currency.

Next, it checks if the show_change argument is True. If it is, it calculates the percentage change between the previous day's rate and the current rate and prints if it's increasing or decreasing. If show_change is False, it simply prints the current rate of the currency.

If the API response status code is not 200, it prints the response error message.
"""

def get_exchange_rate_againts_EUR(currency, show_change=False):
    # Send a GET request to the API URL
    response = requests.get(url)

    # Check if the API request was successful (status code 200)
    if response.status_code == 200:
        # Parse the API response as JSON
        data = response.json()
        # Filter the exchange rate data for the specified currency
        exchange_rates = list(filter(lambda rate: (
            rate['currency'] == currency), data.get('body')))

        # Check if the currency was not found in the exchange rate data
        if not len(exchange_rates):
            print("Please provide the valid currency to be checked against EUR currency.")
            sys.exit(1)

        # Get the exchange rate data for the specified currency
        exchange_rate = exchange_rates[0]

        # If the show_change flag is set to True, calculate and print the percentage change
        if show_change:
            # Call the calculate_percentage_change function to get the percentage change
            percentage_change = calculate_percentage_change(
                exchange_rate['previous_day_rate'], exchange_rate['current_rate'])

            # Check if the percentage change is negative
            if percentage_change < 0:
                print(f"The {currency} rate has decreased by",
                      abs(percentage_change), "%")
            else:
                print(f"The {currency} rate has increased by",
                      percentage_change, "%")
        else:
            # If the show_change flag is not set, simply print the current exchange rate
            print(
                f"The exchange rate of {currency} today is {exchange_rate['current_rate']}")

    else:
        # If the API request was unsuccessful, print the error response
        print(response.json())


if __name__ == '__main__':
    args = sys.argv
    get_exchange_rate_againts_EUR(args[1], bool(args[2]))
