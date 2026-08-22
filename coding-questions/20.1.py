def flatten(data, parent=""):
    result = {}

    if isinstance(data, dict):
        for key, value in data.items():
            path = f"{parent}.{key}" if parent else key
            result.update(flatten(value, path))

    elif isinstance(data, list):
        for i, value in enumerate(data):
            result.update(flatten(value, f"{parent}[{i}]"))

    else:
        result[parent] = data

    return result


# Input
data = {
    "id": 101,
    "name": "Prashant",
    "active": True,

    "address": {
        "city": "Bangalore",
        "country": "India",
        "coordinates": {
            "lat": 12.97,
            "lng": 77.59
        }
    },

    "skills": ["Python", "AWS", "Docker"],

    "projects": [
        {
            "name": "RAG",
            "status": "completed"
        },
        {
            "name": "AI Agent",
            "status": "active"
        }
    ]
}


# Output
print(flatten(data))

"""
{
    "id": 101,
    "name": "Prashant",
    "active": True,
    "address.city": "Bangalore",
    "address.country": "India",
    "address.coordinates.lat": 12.97,
    "address.coordinates.lng": 77.59,
    "skills[0]": "Python",
    "skills[1]": "AWS",
    "skills[2]": "Docker",
    "projects[0].name": "RAG",
    "projects[0].status": "completed",
    "projects[1].name": "AI Agent",
    "projects[1].status": "active"
}
"""