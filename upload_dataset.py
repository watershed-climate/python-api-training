
import os
import requests
import json
import pandas
import readline
import glob

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


def getData(filename):
    df = pandas.read_csv(filename)
    df = df.drop("airline", axis=1)
    return df.to_dict(orient='records')


def getDatasetAndSchemaDetails(filename):
    datasetId = input('What is the dataset ID?\n') # should start with dsetpar_
    schemaId = input('What is the schema ID?\n') # should start with cts_
    schemaVersion = input('What is the schema version?\n')
    return (datasetId, schemaId, schemaVersion)


def uploadFile(filename, measurementProjectId):
    (datasetId, schemaId, schemaVersion) = getDatasetAndSchemaDetails(filename)
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
    data = getData(filename)

    # upload the data
    post(f'v2/ingestion/uploads/{apiUploadId}/data', {"records": data})

    # validate the data
    post(f'v2/ingestion/uploads/{apiUploadId}/validate', {})

    # submit the data
    post(f'v2/ingestion/uploads/{apiUploadId}/submit', { "project_id": measurementProjectId })

# chatgpt helped me with this bit
def input_with_prefill(prompt, text=''):
    def hook():
        readline.insert_text(text)
        readline.redisplay()
    readline.set_pre_input_hook(hook)
    try:
        return input(prompt)
    finally:
        readline.set_pre_input_hook()


def complete(text, state):
    return (glob.glob(os.path.expanduser(text)+'*') + [None])[state]


def get_file_to_process():
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    filename = input_with_prefill("Please enter the file to process: ")
    return filename.strip()


if __name__ == "__main__":
    measurementProjectId = input('What is your measurement project ID?\n') # should start with proj_

    while True:
        filename = get_file_to_process()
        uploadFile(filename, measurementProjectId)
