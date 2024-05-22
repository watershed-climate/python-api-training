from .. import Dataset

## building 4 separate schema "types" for each industry we'll have out of the box demo setup for 

generic_demo = [
    # Buildings - 1 building in each row
    Dataset("data/facilities.csv", "Buildings", "cts_21155GJbgAUG215bB19j", "1.0"),
    # 1 employee per row, with work mode
    Dataset("data/employees.csv", "Employees", "cts_21155GB68XBUiXNU91dc", "1.0"),
    # Grid electricity data
    # Dataset("data/electricity.csv", "Utilities", "cts_21155GF4xvX7L2RNEwHv", "1.0"),

]

healthcare_demo = [
    # Buildings - 1 building in each row
    Dataset("data/facilities.csv", "Buildings", "cts_21155GJbgAUG215bB19j", "1.0")
]

manufacturing_demo = [
    # Buildings - 1 building in each row
    Dataset("data/facilities.csv", "Buildings", "cts_21155GJbgAUG215bB19j", "1.0")
]

food_demo = [
    # Buildings - 1 building in each row
    Dataset("data/facilities.csv", "Buildings", "cts_21155GJbgAUG215bB19j", "1.0")
]