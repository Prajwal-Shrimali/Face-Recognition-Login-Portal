import boto3
import json
import urllib.parse
import requests
import datetime

def construct_federated_url(assume_role_arn, session_name, issuer, sts_client):
    """
    Constructs a URL that gives federated users direct access to the AWS Management Console.
    """
    # Assume the specified role.
    response = sts_client.assume_role(
        RoleArn=assume_role_arn, 
        RoleSessionName=session_name
    )
    temp_credentials = response["Credentials"]
    print(f"Assumed role {assume_role_arn} and got temporary credentials.")

    session_data = {
        "sessionId": temp_credentials["AccessKeyId"],
        "sessionKey": temp_credentials["SecretAccessKey"],
        "sessionToken": temp_credentials["SessionToken"]
    }

    aws_federated_signin_endpoint = "https://signin.aws.amazon.com/federation"

    # Request a sign-in token from AWS federation endpoint.
    response = requests.get(
        aws_federated_signin_endpoint,
        params={
            "Action": "getSigninToken",
            "SessionDuration": str(datetime.timedelta(hours=12).seconds),
            "Session": json.dumps(session_data)
        }
    )
    signin_token = json.loads(response.text)
    print(f"Got a sign-in token from the AWS federation endpoint.")

    # Construct the federated sign-in URL.
    query_string = urllib.parse.urlencode(
        {
            "Action": "login",
            "Issuer": issuer,
            "Destination": "https://console.aws.amazon.com/",
            "SigninToken": signin_token["SigninToken"]
        }
    )
    federated_url = f"{aws_federated_signin_endpoint}?{query_string}"
    return federated_url

def getUserLoginLink(userAccessKey, userSecretAccessKey, roleArn):
    sts_client = boto3.client(
        'sts',
        aws_access_key_id = userAccessKey,
        aws_secret_access_key = userSecretAccessKey
    )
    
    role_arn = roleArn
    session_name = 'TestSession'
    issuer = 'MyApp'

    login_url = construct_federated_url(role_arn, session_name, issuer, sts_client)
    return login_url
    # print(f"Login URL: {login_url}")

# getUserLoginLink("AKIA4SYAMGGCEDAKEOXY", "FY+3jumrqK7C61vfF514G/SaCmiRqY/iIZNsEkJu", "arn:aws:iam::864899838340:role/awsProjectUserRole")