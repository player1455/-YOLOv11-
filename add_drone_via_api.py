#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加无人机信息到数据库，使用Spring Boot API
"""

import requests
import json

def add_drone_via_api():
    """通过Spring Boot API添加无人机信息"""
    base_url = "http://localhost:8080/api"
    
    # 无人机信息
    drone_data = {
        "userId": "test_drone",
        "status": 1,
        "fromAddress": "起始位置",
        "toAddress": "目标位置",
        "completedTaskCount": 0
    }
    
    try:
        # 先登录获取token
        login_response = requests.post(f"{base_url}/login", json={
            'username': 'test_drone_user',
            'password': 'test123'
        })
        
        if login_response.status_code == 200:
            result = login_response.json()
            if result.get("code") == 200:
                token = result.get("data", {}).get("token")
                if token:
                    # 使用token添加无人机信息
                    headers = {
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    }
                    
                    # 尝试创建无人机
                    create_response = requests.post(f"{base_url}/createDrone", json=drone_data, headers=headers)
                    
                    print(f"创建无人机响应状态码: {create_response.status_code}")
                    print(f"创建无人机响应内容: {create_response.text}")
                    
                    if create_response.status_code == 200:
                        create_result = create_response.json()
                        print(f"无人机信息添加成功！")
                        print(f"返回数据: {create_result}")
                    else:
                        print(f"无人机信息添加失败，状态码: {create_response.status_code}")
                else:
                    print(f"登录成功但未获取到token")
            else:
                print(f"登录失败: {result.get('message')}")
        else:
            print(f"登录请求失败，状态码: {login_response.status_code}")
            
    except Exception as e:
        print(f"发生异常: {e}")

if __name__ == "__main__":
    add_drone_via_api()
