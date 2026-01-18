CREATE DATABASE IF NOT EXISTS yolo;

USE yolo;

DROP TABLE IF EXISTS control_log;
DROP TABLE IF EXISTS work_list;
DROP TABLE IF EXISTS drone;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    username VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) PRIMARY KEY NOT NULL,
    user_role VARCHAR(50) NOT NULL COMMENT 'drone, admin, user',
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_role (user_role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE drone (
    user_id VARCHAR(255) PRIMARY KEY NOT NULL,
    status INT DEFAULT 0 COMMENT '0: automatic, 1: manual',
    from_address VARCHAR(255),
    to_address VARCHAR(255),
    completed_task_count INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE work_list (
    task_name VARCHAR(255) NOT NULL,
    task_id VARCHAR(255) PRIMARY KEY NOT NULL,
    from_address VARCHAR(255),
    to_address VARCHAR(255),
    status VARCHAR(50) DEFAULT 'not_accepted' COMMENT 'completed, in_progress, not_accepted',
    accepted_drone_id VARCHAR(255),
    publish_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    accept_time DATETIME,
    completion_time DATETIME,
    FOREIGN KEY (accepted_drone_id) REFERENCES drone(user_id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_accepted_drone_id (accepted_drone_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE control_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    operation_type VARCHAR(100) NOT NULL,
    operation_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    operation_details TEXT,
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_operation_time (operation_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO user (username, user_id, user_role) VALUES
('admin', 'admin001', 'admin'),
('drone1', 'drone001', 'drone'),
('drone2', 'drone002', 'drone'),
('user1', 'user001', 'user');

INSERT INTO drone (user_id, status, from_address, to_address, completed_task_count) VALUES
('drone001', 0, 'america', 'americaa', 100),
('drone002', 0, 'america', 'americaa', 100);

INSERT INTO work_list (task_name, task_id, from_address, to_address, status, accepted_drone_id) VALUES
('Delivery Task 1', 'task001', 'america', 'americaa', 'in_progress', 'drone001'),
('Delivery Task 2', 'task002', 'america', 'americaa', 'not_accepted', NULL);
