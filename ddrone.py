import requests

url = "http://127.0.0.1:8000/v1/repos/11/builds/"

data = {
    "repo": 11,
    "branch": "master"
}

headers = {
    "context-type": "application/json"
}

print("开始触发master分支的构建")
res = requests.post(url=url, data=data, headers=headers)
print("触发结束")
print(res.json())
