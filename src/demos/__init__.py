from collections.abc import MutableSequence
from .. import Dataset
from .demo_1 import demo1

demos: dict[str, MutableSequence[Dataset]] = {
    "demo1": demo1,
    "demo2": demo1,
    "demo3": demo1,
    "demo4": demo1,
}



