import os
import requests

payload = {
  "email": "user@example.com",
  "password": "pwd123",
  "username": "User"
}
res = requests.post('http://api:8000/api/user/create/', data = payload)

print(os.environ.get('USER'))
print(res.status_code)