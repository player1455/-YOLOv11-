#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无人机登录客户端 - 使用电脑模拟无人机
功能：
1. 登录对应的无人机账号（仅校验账号）
2. 上传图片到系统
3. 接受系统指令
"""

import requests
import base64
import json
import time
import cv2
import os

class DroneLoginClient:
    def __init__(self, drone_id, username, base_url="http://localhost:8080/api"):
        """初始化无人机登录客户端
        
        Args:
            drone_id: 无人机ID
            username: 无人机用户名
            base_url: SpringBoot API基础URL
        """
        self.drone_id = drone_id
        self.username = username
        self.base_url = base_url
        self.logged_in = False
        self.token = "test-token"  # 模拟认证令牌
        
        print(f"=== 无人机登录客户端 ===")
        print(f"无人机ID: {drone_id}")
        print(f"用户名: {username}")
        print("=" * 30)
    
    def login(self):
        """登录系统（仅校验账号）
        
        Returns:
            bool: 登录是否成功
        """
        print(f"\n[登录] 校验无人机账号 {self.username} (ID: {self.drone_id})")
        
        try:
            # 发送登录请求（简化为仅校验账号存在）
            response = requests.post(f"{self.base_url}/alldroneInfo", json={'token': self.token})
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200:
                    drones = result.get("data", [])
                    # 检查无人机是否存在
                    for drone in drones:
                        if drone.get("userId") == self.drone_id:
                            print(f"[登录成功] 账号校验通过，无人机 {self.drone_id} 已登录")
                            self.logged_in = True
                            return True
                    
                    print(f"[登录失败] 无人机 {self.drone_id} 不存在")
                else:
                    print(f"[登录失败] 服务器返回错误: {result.get('message')}")
            else:
                print(f"[登录失败] 请求失败，状态码: {response.status_code}")
                
        except Exception as e:
            print(f"[登录失败] 连接服务器失败: {e}")
        
        return False
    
    def image_to_base64(self, image_path):
        """将图片转换为Base64编码
        
        Args:
            image_path: 图片路径
            
        Returns:
            str: Base64编码的图片数据
        """
        if not os.path.exists(image_path):
            print(f"[错误] 图片文件不存在: {image_path}")
            return None
        
        with open(image_path, "rb") as f:
            img_data = f.read()
        
        return base64.b64encode(img_data).decode('utf-8')
    
    def capture_from_camera(self):
        """从电脑摄像头捕获图片
        
        Returns:
            str: Base64编码的图片数据
        """
        print(f"[摄像头] 正在捕获图片...")
        
        # 打开摄像头
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print(f"[错误] 无法打开摄像头")
            return None
        
        # 捕获一帧
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            print(f"[错误] 无法捕获图片")
            return None
        
        # 转换为Base64
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        
        print(f"[摄像头] 图片捕获成功")
        return img_base64
    
    def send_image(self, image_base64):
        """发送图片到系统
        
        Args:
            image_base64: Base64编码的图片数据
            
        Returns:
            dict: 系统返回的指令或结果
        """
        if not self.logged_in:
            print(f"[错误] 请先登录")
            return None
        
        print(f"[发送图片] 正在发送图片到系统...")
        
        try:
            payload = {
                "userId": self.drone_id,
                "image": f"data:image/jpeg;base64,{image_base64}",
                "token": self.token
            }
            
            response = requests.post(f"{self.base_url}/upload", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"[发送成功] 图片已发送，系统返回: {result.get('message')}")
                
                # 将预测结果保存到JSON文件，供前端读取
                data = result.get("data", {})
                self.save_prediction_result(data, image_base64)
                
                return data
            else:
                print(f"[发送失败] 请求失败，状态码: {response.status_code}")
                
        except Exception as e:
            print(f"[发送失败] 发生错误: {e}")
        
        return None
    
    def save_prediction_result(self, result, image_base64):
        """保存预测结果到JSON文件和带标注的图片到固定位置
        
        Args:
            result: 预测结果
            image_base64: 原始图片的Base64编码
        """
        try:
            # 创建结果字典
            prediction_data = {
                "droneId": self.drone_id,
                "username": self.username,
                "timestamp": time.time(),
                "image": image_base64,
                "prediction": result
            }
            
            # 保存到文件
            output_file = f"predictions\prediction_{self.drone_id}.json"
            # 确保目录存在
            os.makedirs("predictions", exist_ok=True)
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(prediction_data, f, ensure_ascii=False, indent=2)
            
            print(f"[保存结果] 预测结果已保存到: {output_file}")
            
            # 保存带标注的图片到固定位置，供前端获取
            # 检查预测结果中是否包含带标注的图片
            if result and isinstance(result, dict):
                # 检查是否有image字段（如果是直接从Flask返回的结果）
                yolo_image_base64 = result.get("image")
                if not yolo_image_base64 and "prediction" in result:
                    # 检查是否嵌套在prediction字段中
                    yolo_image_base64 = result["prediction"].get("image")
                
                if yolo_image_base64:
                    # 确保目录存在
                    os.makedirs("static", exist_ok=True)
                    # 固定位置：static目录下，文件名固定为drone_<drone_id>_yolo.jpg
                    yolo_image_path = f"static\drone_{self.drone_id}_yolo.jpg"
                    
                    # 解码Base64并保存图片
                    if ',' in yolo_image_base64:
                        # 移除可能的前缀
                        yolo_image_base64 = yolo_image_base64.split(',')[1]
                    yolo_image_bytes = base64.b64decode(yolo_image_base64)
                    with open(yolo_image_path, "wb") as f:
                        f.write(yolo_image_bytes)
                    
                    print(f"[保存图片] 带标注的图片已保存到固定位置: {yolo_image_path}")
            
        except Exception as e:
            print(f"[保存失败] 保存预测结果失败: {e}")
    
    def receive_command(self, result_data):
        """接受系统指令
        
        Args:
            result_data: 系统返回的数据
            
        Returns:
            str: 解析后的指令
        """
        if not result_data:
            return "no_command"
        
        # 简化指令解析，根据识别结果生成指令
        boxes = result_data.get("boxes", [])
        
        if len(boxes) == 0:
            command = "continue_flying"
            print(f"[指令] 无障碍物，继续飞行")
        else:
            # 检测到障碍物，生成相应指令
            command = "avoid_obstacle"
            obstacle_count = len(boxes)
            print(f"[指令] 检测到 {obstacle_count} 个障碍物，执行避障操作")
            
            # 简单打印障碍物信息
            for i, box in enumerate(boxes[:3]):  # 只显示前3个障碍物
                class_name = box.get("class_name", "unknown")
                confidence = box.get("confidence", 0)
                print(f"  [{i+1}] {class_name} (置信度: {confidence:.2f})")
            
            if obstacle_count > 3:
                print(f"  ... 还有 {obstacle_count - 3} 个障碍物")
        
        return command
    
    def logout(self):
        """退出登录
        """
        if self.logged_in:
            print(f"[退出] 无人机 {self.drone_id} 已退出")
            self.logged_in = False
        else:
            print(f"[退出] 未登录状态")

def main():
    """主函数"""
    print("=" * 50)
    print("无人机登录客户端")
    print("使用电脑模拟无人机")
    print("=" * 50)
    print("按 Ctrl+C 停止程序")
    print("=" * 50)
    
    # 配置
    drone_id = "drone001"  # 无人机ID
    username = "drone1"    # 无人机用户名
    image_source = "camera"  # 图片来源: camera 或 图片路径
    send_interval = 2.0  # 每次发送图片的间隔时间（秒）
    
    # 创建客户端
    client = DroneLoginClient(drone_id, username)
    
    # 登录（仅校验账号）
    if not client.login():
        print(f"\n[结束] 登录失败，程序退出")
        return
    
    try:
        print(f"\n[开始] 开始连续发送图片，间隔 {send_interval} 秒")
        print("=" * 50)
        
        # 无限循环，持续发送图片
        while True:
            print(f"\n=== 第 {time.strftime('%H:%M:%S')} ===")
            
            # 获取图片数据
            if image_source == "camera":
                image_base64 = client.capture_from_camera()
            else:
                image_base64 = client.image_to_base64(image_source)
            
            if image_base64:
                # 发送图片到系统
                result = client.send_image(image_base64)
                
                if result:
                    # 接受系统指令
                    client.receive_command(result)
                    print(f"[前端显示] 识别结果已发送到前端，可在 http://localhost:5173/flying?userId={drone_id} 查看")
            
            # 等待指定的时间间隔
            print(f"\n[等待] 等待 {send_interval} 秒后发送下一张图片...")
            time.sleep(send_interval)
            
    except KeyboardInterrupt:
        # 用户按 Ctrl+C 停止程序
        print(f"\n\n[结束] 用户停止程序")
    except Exception as e:
        # 其他异常
        print(f"\n\n[错误] 程序发生异常: {e}")
    finally:
        # 退出登录
        client.logout()
        
    print("\n" + "=" * 50)
    print("程序结束")
    print("=" * 50)

if __name__ == "__main__":
    main()
