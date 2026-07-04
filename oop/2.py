# serialization

import json
import pickle

person = {
    "name": "Alice",
    "age": 25
}

# Serialize Python object to JSON string
json_data = json.dumps(person)
print(json_data)

# Deserialize JSON String to Python
person_obj = json.loads(json_data)
print(person_obj["name"])

print("------------")

data = {"name": "Bob", "age": 30}

# Serialize to bytes
serialized = pickle.dumps(data)
print(serialized)

# Deserialize
restored = pickle.loads(serialized)
print(restored)
