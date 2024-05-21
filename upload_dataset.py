import inquirer
from src.demos import demos
from src import post


def get_demo():
    key = "demo"
    questions = [
        inquirer.List(
            key,
            message="What demo would you like to use",
            choices=demos.keys(),
        ),
    ]
    answers = inquirer.prompt(questions)
    return demos[answers[key]]


if __name__ == "__main__":
    demoPath = get_demo()

    measurementProjectId = input('What is your measurement project ID? (hit enter to just make a new project)\n') # should start with proj_
    if (measurementProjectId == ""):
        result = post('v2/ingestion/projects', {
            "name": "New Demo Project",
            "coverageEndDate": "2023-01-01",
            "coverageStartDate": "2022-01-01",
            "kickoff": "2024-05-01",
            "deadline": "2024-06-01"
        })
        measurementProjectId = result["id"]

    for demoFile in demoPath:
        demoFile.upload(measurementProjectId=measurementProjectId)
