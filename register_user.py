#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
注册用户脚本
"""

import requests
import json

def register_user():
    """注册无人机用户"""
    base_url = "http://localhost:8080/api"
    
    # 注册数据
    user_data = {
        "userId": "drone001",
        "username": "drone1",
        "password": "123456",
        "userRole": "drone"
    }
    
    try:
        print("正在注册用户...")
        response = requests.post(f"{base_url}/register", json=user_data)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 200:
                print("注册成功!")
                return True
            else:
                print(f"注册失败: {result.get('message')}")
                return False
        else:
            print(f"注册失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"注册失败: {e}")
        return False

if __name__ == "__main__":
    register_user()
