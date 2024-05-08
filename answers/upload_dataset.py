
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
measurementProjectId = 'proj_2WD5SJYGMzyYTWiDodfF' # should start with proj_
datasetId = 'dsetpar_2WD4757jvtBDjg2cvz5B' # should start with dsetpar_
schemaId = 'cts_21155GFYSXYDGxgNCxmK' # should start with cts_
schemaVersion = '1.0'

if __name__ == "__main__":
    # Example API Query: fetch list of users in the organization
    users = get("v2/organization/users")
    print("Users: ", users)

    ### TODO fill in the below logic

    # create an API upload instance
    createUploadResult = post("v2/ingestion/uploads", {
        "uploadSchemaId": schemaId,
        "uploadSchemaVersion": schemaVersion,
        "datasetId": datasetId,
        "name": "test api upload for workshop"
    })
    print("createUploadResult, ", createUploadResult)

    # store your API upload ID
    apiUploadId = createUploadResult["id"]

    # find your data to upload
    flightsData = getFlightsData()

    # upload the data
    post(f'v2/ingestion/uploads/{apiUploadId}/data', {"records": flightsData})

    # validate the data
    post(f'v2/ingestion/uploads/{apiUploadId}/validate', {})

    # submit the data
    post(f'v2/ingestion/uploads/{apiUploadId}/submit', { "project_id": measurementProjectId })


    # =======================
    # Export a footprint
    # Create the export
    fps = "fps_2WD5CecSURRnzLBK9CUQ"
    createFootprintRequest = post(f'v2/reporting/export', {'footprintSnapshotId': fps})
    print("createFootprintRequest", createFootprintRequest)
    downloadUrl = createFootprintRequest["downloadUrl"]

    print("Polling for export to be ready...")
    while downloadUrl is None:
        downloadUrl = get(f'v2/reporting/export/{createFootprintRequest["id"]}')["downloadUrl"]
    print(downloadUrl)

