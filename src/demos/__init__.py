from collections.abc import MutableSequence
from .. import Dataset
from .demo_1 import generic_demo, healthcare_demo, manufacturing_demo, food_demo

demos: dict[str, MutableSequence[Dataset]] = {
    "generic": generic_demo,
    "healthcare": healthcare_demo,
    "manufacturing": manufacturing_demo,
    "food": food_demo,
}



