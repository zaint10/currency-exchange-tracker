# Currency Exchange Tracking Application
This application provides the current exchange rates for various currencies and their change compared to the previous day. The data is fetched every day from the European Central Bank (ECB) and stored in a DynamoDB database.

# Getting Started
These instructions will get you a copy of the project up and running on your local machine or in the cloud (AWS).

# Prerequisites
You need to have the following software installed on your local machine:

- Python 3.x
- AWS CLI
- AWS SAM CLI
- An AWS account with sufficient permissions to deploy the required services

Installing

Clone this repository to your local machine

```
    git clone https://github.com/<repository-url>
```

cd into the project directory

```
    cd currency-exchange-tracking
```

Install the required Python packages
```
    pip install -r requirements.txt
```

# Deployment

To deploy the application to your AWS environment, follow these steps:

1. Package the application using AWS SAM
```
    sam package --output-template-file packaged.yml --s3-bucket <your-s3-bucket>
```
2. Deploy the application to AWS using AWS SAM
```
    sam deploy --template-file packaged.yml --stack-name <your-stack-name> --capabilities CAPABILITY_IAM
```

# Usage
You can access the REST API by sending a GET request to the URL provided in the outputs section of the CloudFormation stack.

The REST API endpoint returns the exchange rate information for the every currency

To see the current exchange rate of a currency against the EUR, I have written a main.py file that will test the API and return the rate for the currency specified in the argument

To see the current exchange rate of a USD currency against the EUR, run a python script

```
    python main.py 'USD'
```

To see the current exchange rate of a USD currency against the EUR and its chnaged from previous day, run a python script

```
    python main.py 'USD' True
```