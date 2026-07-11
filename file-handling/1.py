import json
import csv
import os

with open('./test.md') as f:
    print(f.read())
    
if os.path.exists("ChangedFile.csv"):
    os.remove("ChangedFile.csv")
    print("File Removed!")


data = {"name": "Aakash", "age": 20}
with open("data.json", "w") as f:
    json.dump(data, f)


with open("data.json") as f:
    print(json.load(f))

with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])
    writer.writerow(["Aakash", 20])

