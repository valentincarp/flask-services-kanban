import requests

url = "http://127.0.0.1:5004/upload/csv"

with open("../data/donnees_exemple.csv", "rb") as f:
    files = {
        "file": f
    }

    response = requests.post(url, files=files)

print(response.status_code)
print(response.json())