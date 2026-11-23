import requests

url = "http://127.0.0.1:5000/predict"

data = {
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 25.5,
    "humidity": 80,
    "ph": 6.5,
    "rainfall": 200
}

response = requests.post(url, json=data)

print("\nStatus Code:")
print(response.status_code)

print("\nPrediction Result:")
print(response.json())