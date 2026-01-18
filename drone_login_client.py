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
import threading
from datetime import datetime
import cv2
import os
import queue
import aiohttp
import asyncio

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
        
        # 线程相关属性
        self.image_queue = queue.Queue(maxsize=20)  # 图片队列，最大20张，增加缓冲区
        self.running = False  # 运行状态标志
        self.send_thread = None  # 发送线程
        self.capture_thread = None  # 捕获线程
        self.image_counter = 0  # 图片计数器，用于显示发送速率
        
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
            # 简化登录逻辑，直接使用droneInfo接口检查单个无人机是否存在
            response = requests.post(f"{self.base_url}/droneInfo", json={'userId': self.drone_id, 'token': self.token})
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 200:
                    drone = result.get("data", {})
                    if drone:
                        print(f"[登录成功] 账号校验通过，无人机 {self.drone_id} 已登录")
                        self.logged_in = True
                        return True
                    else:
                        print(f"[登录失败] 无人机 {self.drone_id} 不存在")
                elif result.get("code") == 404:
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
        try:
            # 打开摄像头（如果没有打开的话）
            if not hasattr(self, 'cap') or not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
                # 设置摄像头属性，提高捕获速度
                self.cap.set(cv2.CAP_PROP_FPS, 15)  # 设置FPS为15
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 降低分辨率
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                
                if not self.cap.isOpened():
                    return None
            
            # 捕获一帧
            ret, frame = self.cap.read()
            if not ret:
                return None
            
            # 转换为Base64，降低质量，加快传输
            _, img_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            img_base64 = base64.b64encode(img_encoded).decode('utf-8')
            
            return img_base64
        except Exception as e:
            return None
    
    async def async_send_image(self, image_base64, session):
            """异步发送图片到系统，优化发送逻辑
            
            Args:
                image_base64: Base64编码的图片数据
                session: aiohttp客户端会话
                
            Returns:
                None: 不返回结果，提高发送速度
            """
            if not self.logged_in:
                return None
            
            try:
                payload = {
                    "userId": self.drone_id,
                    "image": f"data:image/jpeg;base64,{image_base64}",
                    "token": self.token
                }
                
                # 发送请求并处理响应
                async with session.post(
                    f"{self.base_url}/upload", 
                    json=payload, 
                    timeout=1.0
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        data = result.get("data", {})
                        self.save_prediction_result(data, image_base64)
                        self.receive_command(data)
                
                # 无论成功失败，都递增计数器，用于统计发送速率
                self.image_counter += 1
            except Exception as e:
                # 发生异常，也递增计数器
                self.image_counter += 1
                pass
            
            return None
    
    def send_image(self, image_base64):
        """同步发送图片到系统（保留原有接口，供其他地方调用）
        
        Args:
            image_base64: Base64编码的图片数据
            
        Returns:
            dict: 系统返回的指令或结果
        """
        if not self.logged_in:
            print(f"[错误] 请先登录")
            return None
        
        try:
            payload = {
                "userId": self.drone_id,
                "image": f"data:image/jpeg;base64,{image_base64}",
                "token": self.token
            }
            
            response = requests.post(f"{self.base_url}/upload", json=payload, timeout=2.0)
            
            if response.status_code == 200:
                result = response.json()
                data = result.get("data", {})
                self.save_prediction_result(data, image_base64)
                return data
        except Exception as e:
            pass
        
        return None
    
    def cleanup_old_images(self, image_dir, max_age_seconds=3):
        """清理指定目录下超过指定时间的旧图片
        
        Args:
            image_dir: 图片目录
            max_age_seconds: 图片最大保留时间（秒）
        """
        if not os.path.exists(image_dir):
            return
        
        current_time = time.time()
        deleted_count = 0
        
        for filename in os.listdir(image_dir):
            if filename.endswith('.jpg') and filename.startswith(self.drone_id):
                file_path = os.path.join(image_dir, filename)
                file_age = current_time - os.path.getmtime(file_path)
                
                if file_age > max_age_seconds:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        pass
        
        # 只在有图片被删除时打印，减少控制台输出
        if deleted_count > 0:
            print(f"[清理图片] 删除了 {deleted_count} 张过期图片")
    
    def save_prediction_result(self, result, image_base64):
        """保存预测结果到固定位置，按时间戳命名，并清理旧图片
        
        Args:
            result: 预测结果
            image_base64: 原始图片的Base64编码
        """
        try:
            # 检查预测结果中是否包含带标注的图片
            if result and isinstance(result, dict):
                # 检查是否有image字段（如果是直接从Flask返回的结果）
                yolo_image_base64 = result.get("image")
                if not yolo_image_base64 and "prediction" in result:
                    # 检查是否嵌套在prediction字段中
                    yolo_image_base64 = result["prediction"].get("image")
                
                if yolo_image_base64:
                    # 创建无人机专用目录
                    image_dir = os.path.join("static", "drone_images", self.drone_id)
                    os.makedirs(image_dir, exist_ok=True)
                    
                    # 生成时间戳文件名
                    now = datetime.now()
                    timestamp = now.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # 精确到毫秒
                    image_filename = f"{self.drone_id}_{timestamp}.jpg"
                    image_path = os.path.join(image_dir, image_filename)
                    
                    # 解码Base64并保存图片
                    if ',' in yolo_image_base64:
                        # 移除可能的前缀
                        yolo_image_base64 = yolo_image_base64.split(',')[1]
                    yolo_image_bytes = base64.b64decode(yolo_image_base64)
                    with open(image_path, "wb") as f:
                        f.write(yolo_image_bytes)
                    
                    # 不再清理旧图片，保存所有检测过的图片
                    # self.cleanup_old_images(image_dir, max_age_seconds=3)
                    
                    # 保存最新图片链接到固定位置，供前端快速访问
                    latest_image_path = os.path.join("static", f"drone_{self.drone_id}_yolo.jpg")
                    with open(latest_image_path, "wb") as f:
                        f.write(yolo_image_bytes)
            
        except Exception as e:
            pass
    
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
    
    def capture_images(self):
        """持续捕获图片的线程方法"""
        print(f"[线程启动] 图片捕获线程已启动")
        
        # 性能优化：减少重复的摄像头初始化检查
        camera_initialized = False
        cap = None
        
        try:
            cap = cv2.VideoCapture(0)
            # 设置摄像头属性，提高捕获速度
            cap.set(cv2.CAP_PROP_FPS, 30)  # 提高FPS到30
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # 进一步降低分辨率
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 减少缓冲区，降低延迟
            
            if cap.isOpened():
                camera_initialized = True
                print(f"[摄像头] 成功初始化，分辨率: 320x240, FPS: 30")
            else:
                print(f"[摄像头] 无法打开")
        except Exception as e:
            print(f"[摄像头] 初始化错误: {e}")
        
        # 预生成时间戳，减少每次循环的计算
        last_capture_time = time.time()
        target_interval = 0.4  # 0.4秒捕获一次，进一步降低发送速率
        
        # 添加捕获计数器
        capture_count = 0
        start_time = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                elapsed = current_time - last_capture_time
                
                if elapsed >= target_interval:
                    if camera_initialized and cap:
                        # 捕获一帧，不等待
                        cap.grab()  # 只抓取帧，不解码
                        ret, frame = cap.retrieve()  # 解码帧
                        
                        if ret:
                            capture_count += 1
                            
                            # 快速编码为JPEG，进一步降低质量和分辨率
                            # 先缩放图片到更小尺寸
                            small_frame = cv2.resize(frame, (160, 120))
                            
                            # 快速编码为JPEG，使用更低的质量
                            _, img_encoded = cv2.imencode('.jpg', small_frame, [
                                int(cv2.IMWRITE_JPEG_QUALITY), 30,  # 降低质量到30
                                int(cv2.IMWRITE_JPEG_PROGRESSIVE), 0,  # 禁用渐进式
                                int(cv2.IMWRITE_JPEG_OPTIMIZE), 0,  # 禁用优化
                                int(cv2.IMWRITE_JPEG_LUMA_QUALITY), 30,  # 亮度质量
                                int(cv2.IMWRITE_JPEG_CHROMA_QUALITY), 30  # 色度质量
                            ])
                            
                            # 更快的Base64编码，使用更快的编码方式
                            img_base64 = base64.b64encode(img_encoded).decode('ascii', 'ignore')
                            
                            if img_base64:
                                # 尝试将图片放入队列，如果队列已满则跳过
                                try:
                                    self.image_queue.put(img_base64, block=False)
                                except queue.Full:
                                    # 队列已满，跳过当前图片，增加调试信息
                                    pass
                        
                    last_capture_time = current_time
                else:
                    # 短暂休息，让出CPU，但不要阻塞
                    time.sleep(0.001)
            except Exception as e:
                print(f"[捕获错误] {e}")
                time.sleep(0.005)
            
            # 每5秒打印一次捕获速率
            if time.time() - start_time >= 5.0:
                capture_rate = capture_count / (time.time() - start_time)
                print(f"[捕获速率] 实际捕获速率: {capture_rate:.1f} 张/秒")
                print(f"[队列状态] 当前队列大小: {self.image_queue.qsize()}")
                # 重置计数器
                capture_count = 0
                start_time = time.time()
        
        # 释放摄像头
        if cap:
            try:
                cap.release()
            except:
                pass
        
        print(f"[线程结束] 图片捕获线程已结束")
    
    def send_images(self):
        """持续发送图片的线程方法，使用异步IO提高发送速度"""
        print(f"[线程启动] 图片发送线程已启动")
        
        async def async_send_task(image_base64, session):
            """单个图片发送任务"""
            if image_base64:
                result = await self.async_send_image(image_base64, session)
                if result:
                    self.receive_command(result)
        
    def send_images(self):
        """持续发送图片的线程方法，使用异步IO提高发送速度"""
        print(f"[线程启动] 图片发送线程已启动")
        
        async def async_send_batch(images, session):
            """批量发送图片"""
            if not images:
                return
            
            # 创建所有发送任务
            tasks = [self.async_send_image(image, session) for image in images]
            # 并行执行所有任务
            await asyncio.gather(*tasks, return_exceptions=True)
        
        async def async_send_loop():
            """异步发送循环，并行处理多张图片"""
            # 创建一个TCP连接器，增加连接池大小
            connector = aiohttp.TCPConnector(
                limit=200,  # 增加连接池大小
                limit_per_host=100,  # 每个主机的连接数
                ttl_dns_cache=300,  # DNS缓存时间
                enable_cleanup_closed=True  # 启用关闭连接清理
            )
            
            async with aiohttp.ClientSession(connector=connector) as session:
                while self.running:
                    try:
                        # 批量获取队列中的图片，每次获取5张
                        batch_images = []
                        for _ in range(5):
                            try:
                                image = self.image_queue.get(block=True, timeout=0.01)
                                if image:
                                    batch_images.append(image)
                            except queue.Empty:
                                break
                        
                        if batch_images:
                            # 并行发送批量图片
                            await async_send_batch(batch_images, session)
                        else:
                            # 队列为空，短暂休息
                            await asyncio.sleep(0.001)
                    except Exception as e:
                        await asyncio.sleep(0.001)
        
        # 运行异步循环
        asyncio.run(async_send_loop())
        
        print(f"[线程结束] 图片发送线程已结束")
    
    def start_continuous_send(self):
        """启动持续发送图片的线程"""
        if not self.logged_in:
            print(f"[错误] 请先登录")
            return False
        
        self.running = True
        self.image_counter = 0
        
        # 启动捕获线程
        self.capture_thread = threading.Thread(target=self.capture_images, daemon=True)
        self.capture_thread.start()
        
        # 启动发送线程
        self.send_thread = threading.Thread(target=self.send_images, daemon=True)
        self.send_thread.start()
        
        # 启动速率统计线程
        self.rate_counter_thread = threading.Thread(target=self.rate_counter, daemon=True)
        self.rate_counter_thread.start()
        
        # 增加调试信息，显示队列大小
        print(f"[启动成功] 已启动持续发送图片，目标速率：10张/秒")
        print(f"[队列信息] 初始队列大小: {self.image_queue.qsize()}, 最大容量: {self.image_queue.maxsize}")
        return True
    
    def stop_continuous_send(self):
        """停止持续发送图片的线程"""
        self.running = False
        
        # 释放摄像头
        if hasattr(self, 'cap'):
            try:
                self.cap.release()
            except:
                pass
        
        # 等待线程结束
        if hasattr(self, 'capture_thread') and self.capture_thread:
            self.capture_thread.join(timeout=1.0)
        if hasattr(self, 'send_thread') and self.send_thread:
            self.send_thread.join(timeout=1.0)
        if hasattr(self, 'rate_counter_thread') and self.rate_counter_thread:
            self.rate_counter_thread.join(timeout=1.0)
        
        # 清空队列
        while not self.image_queue.empty():
            try:
                self.image_queue.get(block=False)
            except queue.Empty:
                pass
        
        print(f"[停止成功] 已停止持续发送图片")
    
    def rate_counter(self):
        """统计发送速率"""
        while self.running:
            start_time = time.time()
            start_count = self.image_counter
            
            # 等待1秒
            time.sleep(1.0)
            
            end_time = time.time()
            end_count = self.image_counter
            
            # 计算实际速率
            elapsed = end_time - start_time
            sent = end_count - start_count
            rate = sent / elapsed
            
            print(f"[速率统计] 实际发送速率: {rate:.1f} 张/秒 (1秒内发送了 {sent} 张)")
    
    def logout(self):
        """退出登录
        """
        self.stop_continuous_send()
        
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
    
    # 创建客户端
    client = DroneLoginClient(drone_id, username)
    
    # 登录（仅校验账号）
    if not client.login():
        print(f"\n[结束] 登录失败，程序退出")
        return
    
    try:
        print(f"\n[开始] 开始持续发送图片，每0.1秒发送一张")
        print("=" * 50)
        
        # 启动持续发送图片
        client.start_continuous_send()
        
        # 主线程保持运行，直到用户按 Ctrl+C
        while True:
            time.sleep(1.0)  # 主线程每1秒检查一次
            
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
