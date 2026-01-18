import requests
import json

# 1. 为数据库添加示例数据
# 我们可以直接调用SpringBoot的API来添加数据

def add_sample_data():
    base_url = "http://localhost:8080/api"

    # 添加用户数据
    users = [
        {
            "username": "admin",
            "userId": "admin001",
            "userRole": "admin"
        },
        {
            "username": "drone1",
            "userId": "drone001",
            "userRole": "drone"
        },
        {
            "username": "drone2",
            "userId": "drone002",
            "userRole": "drone"
        },
        {
            "username": "user1",
            "userId": "user001",
            "userRole": "user"
        }
    ]

    # 添加无人机数据
    drones = [
        {
            "userId": "drone001",
            "status": 0,
            "fromAddress": "america",
            "toAddress": "americaa",
            "completedTaskCount": 100
        },
        {
            "userId": "drone002",
            "status": 0,
            "fromAddress": "america",
            "toAddress": "americaa",
            "completedTaskCount": 100
        }
    ]

    # 添加任务数据
    tasks = [
        {
            "taskName": "Delivery Task 1",
            "taskId": "task001",
            "fromAddress": "america",
            "toAddress": "americaa",
            "status": "in_progress",
            "acceptedDroneId": "drone001"
        },
        {
            "taskName": "Delivery Task 2",
            "taskId": "task002",
            "fromAddress": "america",
            "toAddress": "americaa",
            "status": "not_accepted"
        }
    ]

    # 创建用户
    for user in users:
        try:
            response = requests.post(f"{base_url}/createUser", json=user)
            print(f"Created user {user['username']}: {response.status_code}")
        except Exception as e:
            print(f"Error creating user {user['username']}: {e}")

    print("\nSample data added successfully!")

# 2. 调用YOLO识别API的示例
def call_yolo_api():
    # YOLO API URL
    yolo_url = "http://localhost:5001/predict"

    # 示例：如何调用YOLO API
    print("\n=== YOLO API调用说明 ===")
    print(f"API URL: {yolo_url}")
    print("请求方法: POST")
    print("请求格式: JSON")
    print("请求参数:")
    print("{")
    print("  'userId': 'drone001',        # 无人机ID")
    print("  'image': 'base64_image_data', # Base64编码的图像数据")
    print("  'token': 'test-token'        # 认证令牌（可选）")
    print("}")

    print("\n返回格式:")
    print("{")
    print("  'code': 200,")
    print("  'message': 'success',")
    print("  'data': {")
    print("    'boxes': [                # 检测到的障碍物列表")
    print("      {")
    print("        'xyxy': [x1, y1, x2, y2], # 边界框坐标")
    print("        'confidence': 0.95,     # 置信度")
    print("        'class': 0,             # 类别ID")
    print("        'class_name': 'person'   # 类别名称")
    print("      }")
    print("    ],")
    print("    'image': 'base64_image'    # 带标注的图像")
    print("  }")
    print("}")

    print("\n=== 示例代码 ===")
    print("import requests")
    print("import base64")
    print("from PIL import Image")
    print("import io")
    print()
    print("# 1. 读取图像并转换为Base64")
    print("def image_to_base64(image_path):")
    print("    with open(image_path, 'rb') as f:")
    print("        img_data = f.read()")
    print("    return base64.b64encode(img_data).decode('utf-8')")
    print()
    print("# 2. 调用YOLO API")
    print("def detect_obstacles(image_path, drone_id):")
    print("    url = 'http://localhost:5001/predict'")
    print("    image_base64 = image_to_base64(image_path)")
    print()
    print("    payload = {")
    print("        'userId': drone_id,")
    print("        'image': image_base64,")
    print("        'token': 'test-token'")
    print("    }")
    print()
    print("    response = requests.post(url, json=payload)")
    print("    return response.json()")
    print()
    print("# 3. 使用示例")
    print("result = detect_obstacles('test.jpg', 'drone001')")
    print("print(result['data']['boxes'])  # 打印检测到的障碍物")

if __name__ == "__main__":
    add_sample_data()
    call_yolo_api()
