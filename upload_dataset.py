
import os
import requests
import json
import pandas


env_token = os.getenv("WATERSHED_API_KEY")
token = env_token if env_token else ""


def fullUrl(url):
    return "https://api.watershedclimate.com/"+url


headers = {
  'accept': 'application/json',
  'content-type': 'application/json',
  'authorization': 'Bearer '+token,
}


def get(url):
    print("")
    print("GET query to "+fullUrl(url))
    request = requests.get(fullUrl(url), headers=headers)
    print(f'-> reponse: {request.status_code}')
    if request.status_code > 300:
        print(f'-> error: {request.text}')
    return request.json()


def post(url, body):
    print("")
    print("POST query to "+fullUrl(url))
    request = requests.post(fullUrl(url), headers=headers, data=json.dumps(body))
    print(f'-> reponse: {request.status_code}')
    if request.status_code > 300:
        print(f'-> error: {request.text}')
    return request.json()


def getFlightsData():
    df = pandas.read_csv("Flights.csv")
    df = df.drop("airline", axis=1)
    return df.to_dict(orient='records')


# TODO find these variables
measurement_project_id = ''
dataset_id = ''
cts_id = ''
cts_version_id = ''

if __name__ == "__main__":
    # Example API Query: fetch list of users in the organization
    users = get("v2/organization/users")
    print("Users: ", users)

    ### TODO fill in the below logic

    # create an API upload instance

    # get your API upload ID

    # get your data to upload

    # upload the data

    # validate the data

    # submit the data
