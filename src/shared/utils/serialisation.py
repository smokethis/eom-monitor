import json
from dataclasses import asdict, is_dataclass
from enum import Enum

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        return super().default(obj)

def serialize(obj):
    if is_dataclass(obj):
        obj = asdict(obj) # type: ignore

    return obj

def pretty_json(obj):
    return json.dumps(
        serialize(obj),
        indent=4,
        sort_keys=True,
        cls=EnumEncoder
    )