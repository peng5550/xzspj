import requests



url = "http://127.0.0.1:8888/verify"
response = requests.post(url, data={"code":123456})
print(response.text)