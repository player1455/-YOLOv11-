#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加无人机信息到数据库
"""

import mysql.connector
from mysql.connector import Error

def add_drone():
    """添加无人机信息到数据库"""
    try:
        # 连接数据库
        connection = mysql.connector.connect(
            host='localhost',
            database='yolo',
            user='root',
            password='123456'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 插入无人机记录
            insert_query = """
            INSERT INTO drone (user_id, status, from_address, to_address, completed_task_count)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, ('test_drone', 1, '起始位置', '目标位置', 0))
            
            # 提交事务
            connection.commit()
            
            # 验证插入结果
            cursor.execute("SELECT * FROM drone WHERE user_id = %s", ('test_drone',))
            result = cursor.fetchall()
            
            print("无人机信息添加成功！")
            print("查询结果：")
            for row in result:
                print(f"  user_id: {row[0]}")
                print(f"  status: {row[1]}")
                print(f"  from_address: {row[2]}")
                print(f"  to_address: {row[3]}")
                print(f"  completed_task_count: {row[4]}")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"数据库错误: {e}")
    except Exception as e:
        print(f"发生异常: {e}")

if __name__ == "__main__":
    add_drone()
