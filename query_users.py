#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询数据库中的用户信息
"""

import mysql.connector
from mysql.connector import Error

def query_users():
    """查询数据库中的用户信息"""
    try:
        # 连接数据库
        connection = mysql.connector.connect(
            host='localhost',
            database='yolo',
            user='root',
            password='123456'
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # 查询所有用户
            cursor.execute("SELECT * FROM user")
            users = cursor.fetchall()
            
            print("数据库中的用户信息：")
            for user in users:
                print(f"用户ID: {user['user_id']}")
                print(f"用户名: {user['username']}")
                print(f"密码: {user['password']}")
                print(f"角色: {user['user_role']}")
                print(f"创建时间: {user['creation_date']}")
                print("-" * 30)
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"数据库错误: {e}")

if __name__ == "__main__":
    query_users()
