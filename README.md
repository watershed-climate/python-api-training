# Watershed API Example

This repository contains example code to demonstrate how the Watershed API can be used. 


## Setup
Watershed Access
1. Make sure you have access to a staging or test Watershed environment. The training will upload data to Watershed, so we don't want to disrupt a production measurement.
1. Log into Watershed at [dashboard.watershedclimate.com](https://dashboard.watershedclimate.com)
1. Create an API key in [the Organization Settings page](https://dashboard.watershedclimate.com/settings/api)


Training Repo Setup
1. Make sure your system has [poetry](https://python-poetry.org/docs/#installation) installed
1. Clone this repository locally
1. Run `./scripts/setup`
1. Enter your API key when prompted. This will be saved to a `secrets.env` file so that your API scripts can use it later. 

## Training Instructions 
1. Open `upload_dataset.py`, which has some sample code for sending API requests, as well as an example request at the bottom.
1. Run `./scripts/run` to execute `upload_dataset.py`
1. Refer to [Watershed's API documentation](https://api-docs.watershed.com/reference)
1. Fill out the remaining functionality specified in the comments

## Resources
- [Watershed's learning hub](https://dashboard.watershedclimate.com/learn#)
- [API Documentation](https://api-docs.watershed.com/reference)
- Please contact api-support@watershedclimate.com for any questions
