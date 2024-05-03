
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
    df = pandas.read_csv("Flights_ Flights by distance.csv")
    df = df.drop("airline", axis=1)
    return df.to_dict(orient='records')


measurement_project_id = 'proj_2WD5RRZSX1E5uBNGRL1Y'
dataset_id = 'dsetpar_2WD4757jvtBDjg2cvz5B'
cts_id = 'cts_21155GFYSXYDGxgNCxmK'
cts_version_id = 'ctsv_2115KzYR4J2XsDHT6CcA'


if __name__ == "__main__":
    # confirm API connectivity by querying for list of users in your organization
    users = get("v2/organization/users")
    print("users", users)

    # create an API upload instance
    apiUpload = post("v2/ingestion/uploads", {
        "uploadSchemaId": cts_id,
        "uploadSchemaVersion": cts_version_id,
        "datasetId": dataset_id,
    })

    print(apiUpload)
    # get your API upload ID
    apiUploadId = apiUpload["id"]


    # get your data to upload
    flightsData = getFlightsData()
    print("")
    print("Generated flights data:")
    print(flightsData)

    # upload the data
    dataResult = post(
        f'v2/ingestion/uploads/{apiUploadId}/data',
        {'records':flightsData}
    )

    # validate the data
    apiUploadValidation = post(f'v2/ingestion/uploads/{apiUploadId}/validate', {})
    print("apiUpload", apiUploadValidation)

    # submit the data
    apiUploadSubmission = post(f'v2/ingestion/uploads/{apiUploadId}/submit', {'project_id': measurement_project_id})
    print("apiUpload", apiUploadSubmission)

