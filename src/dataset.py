
import os
import requests
import json
import pandas
from attrs import define


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
    print("here", token, body)
    print("POST query to "+fullUrl(url))
    request = requests.post(fullUrl(url), headers=headers, data=json.dumps(body))
    print(f'-> reponse: {request.status_code}')
    if request.status_code > 300:
        print(f'-> error: {request.text}')
    return request.json()


def getData(filename):
    df = pandas.read_csv(filename, keep_default_na=False)
    return df.to_dict(orient='records')


@define
class Dataset:
    filename: str
    datasetName: str
    schemaId: str
    schemaVersion: str

    def upload(self, measurementProjectId: str):
        datasets = get("v2/ingestion/datasets")
        matching_datasets = filter(lambda dataset: dataset['node']["name"] == self.datasetName, datasets["edges"])
        dataset = next(matching_datasets, None)
        datasetId = dataset['node']["id"] if dataset else None

        # create an API upload instance
        createUploadResult = post("v2/ingestion/uploads", {
            "uploadSchemaId": self.schemaId,
            "uploadSchemaVersion": self.schemaVersion,
            "datasetId": datasetId,
        })
        print("createUploadResult, ", createUploadResult)

        # store your API upload ID
        apiUploadId = createUploadResult["id"]

        # find your data to upload
        data = getData(self.filename)

        # upload the data
        post(f'v2/ingestion/uploads/{apiUploadId}/data', {"records": data})

        # validate the data
        post(f'v2/ingestion/uploads/{apiUploadId}/validate', {})

        # submit the data
        post(f'v2/ingestion/uploads/{apiUploadId}/submit', { "project_id": measurementProjectId })

