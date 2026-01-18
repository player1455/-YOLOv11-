import requests
import base64

# 读取一张测试图片
with open('test.jpg', 'rb') as f:
    image_data = f.read()

# 转换为base64
base64_image = base64.b64encode(image_data).decode('utf-8')

# 发送请求到predict接口
url = 'http://localhost:5001/predict'
headers = {'Content-Type': 'application/json'}
data = {
    'userId': 'drone001',
    'image': f'data:image/jpeg;base64,{base64_image}',
    'token': 'test-token'
}

response = requests.post(url, headers=headers, json=data)
print(f"Response status: {response.status_code}")
print(f"Response content: {response.json()}")
