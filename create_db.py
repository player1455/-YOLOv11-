import mysql.connector

# 使用提供的凭据连接到MySQL服务器
try:
    # 先连接到MySQL服务器（不指定数据库）
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456'
    )
    
    if connection.is_connected():
        cursor = connection.cursor()
        
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS yolo")
        print("Database 'yolo' created successfully")
        
        # 切换到创建的数据库
        cursor.execute("USE yolo")
        
        # 创建表（简化版，主要字段）
        
        # user表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            username VARCHAR(255) NOT NULL,
            user_id VARCHAR(255) PRIMARY KEY NOT NULL,
            user_role VARCHAR(50) NOT NULL COMMENT 'drone, admin, user',
            creation_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("Table 'user' created successfully")
        
        # drone表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS drone (
            user_id VARCHAR(255) PRIMARY KEY NOT NULL,
            status INT DEFAULT 0 COMMENT '0: automatic, 1: manual',
            from_address VARCHAR(255),
            to_address VARCHAR(255),
            completed_task_count INT DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
        )
        """)
        print("Table 'drone' created successfully")
        
        # work_list表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS work_list (
            task_name VARCHAR(255) NOT NULL,
            task_id VARCHAR(255) PRIMARY KEY NOT NULL,
            from_address VARCHAR(255),
            to_address VARCHAR(255),
            status VARCHAR(50) DEFAULT 'not_accepted' COMMENT 'completed, in_progress, not_accepted',
            accepted_drone_id VARCHAR(255),
            publish_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            accept_time DATETIME,
            completion_time DATETIME,
            FOREIGN KEY (accepted_drone_id) REFERENCES drone(user_id) ON DELETE SET NULL
        )
        """)
        print("Table 'work_list' created successfully")
        
        # control_log表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS control_log (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            operation_type VARCHAR(100) NOT NULL,
            operation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            operation_details TEXT,
            FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
        )
        """)
        print("Table 'control_log' created successfully")
        
        # 插入示例数据
        cursor.execute("INSERT IGNORE INTO user (username, user_id, user_role) VALUES ('admin', 'admin001', 'admin')")
        cursor.execute("INSERT IGNORE INTO user (username, user_id, user_role) VALUES ('drone1', 'drone001', 'drone')")
        cursor.execute("INSERT IGNORE INTO user (username, user_id, user_role) VALUES ('drone2', 'drone002', 'drone')")
        cursor.execute("INSERT IGNORE INTO user (username, user_id, user_role) VALUES ('user1', 'user001', 'user')")
        
        cursor.execute("INSERT IGNORE INTO drone (user_id, status, from_address, to_address, completed_task_count) VALUES ('drone001', 0, 'america', 'americaa', 100)")
        cursor.execute("INSERT IGNORE INTO drone (user_id, status, from_address, to_address, completed_task_count) VALUES ('drone002', 0, 'america', 'americaa', 100)")
        
        connection.commit()
        print("Sample data inserted successfully")
        
except mysql.connector.Error as e:
    print(f"Error: {e}")
    
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed")
