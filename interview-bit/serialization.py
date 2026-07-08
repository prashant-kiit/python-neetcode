import pickle

data = {"name": "Alice", "age": 25}

# Serialize (object -> bytes -> file)
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

# Deserialize (file -> bytes -> object)
with open("data.pkl", "rb") as f:
    obj = pickle.load(f)

print(obj)

# Serialization = Object → Storable/Transmittable format
# Deserialization = Stored/Transmitted format → Object