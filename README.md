# YOLO无人机障碍规避系统 - 开发文档

## 项目概述

本项目是一个基于YOLOv11的无人机障碍规避系统，采用前后端分离架构，实现无人机实时监控、障碍物检测和避障功能。

### 核心功能

- 用户注册和登录认证
- 无人机实时监控
- 障碍物检测和识别
- 避障指令生成
- 实时视频流显示
- 历史记录查询

### 技术特点

- 基于SHA256的token加密机制
- 异步图片处理和传输
- 多线程并发处理
- 实时视频流推送
- 前端路由守卫和权限控制

## 系统架构

### 整体架构

```
┌─────────────┐
│   前端Vue    │
│   (端口5173)   │
└──────┬──────┘
       │
       │
       ▼
┌─────────────┐
│  Spring Boot  │
│   (端口8080)   │
└──────┬──────┘
       │
       │
       ▼
┌─────────────┐
│  Flask YOLO   │
│   (端口5001)   │
└─────────────┘
       │
       ▼
┌─────────────┐
│  MySQL数据库  │
│   (端口3306)   │
└─────────────┘
```

### 数据流向

1. **用户登录流程**：
   - 前端 → Spring Boot: `/api/login`
   - Spring Boot验证用户名和密码
   - Spring Boot生成SHA256加密的token
   - 返回token和用户信息
   - 前端保存token到localStorage

2. **无人机客户端登录流程**：
   - 客户端 → Spring Boot: `/api/login`
   - Spring Boot验证用户名和密码
   - Spring Boot生成SHA256加密的token
   - 返回token和用户信息
   - 客户端保存token到内存

3. **图片上传和检测流程**：
   - 客户端 → Spring Boot: `/api/upload`
   - Spring Boot转发到Flask: `/predict`
   - Flask使用YOLOv11进行障碍物检测
   - Flask返回检测结果和标注图片
   - Flask保存图片到`./static/drone_images/`目录
   - Spring Boot返回结果给客户端

4. **前端视频流流程**：
   - 前端 → Flask: `/flask/latest_image/<user_id>`
   - Flask从缓存或文件系统读取最新图片
   - Flask返回图片数据
   - 前端显示图片

## 技术栈

### 后端

#### Spring Boot
- **版本**: Spring Boot 3.x
- **Java版本**: Java 17+
- **数据库**: MySQL 8.0
- **ORM**: Spring Data JPA
- **构建工具**: Maven

#### Flask
- **版本**: Python 3.x
- **Web框架**: Flask
- **AI模型**: YOLOv11
- **Web服务器**: waitress
- **图像处理**: OpenCV, Pillow

### 前端

- **框架**: Vue 3
- **构建工具**: Vite
- **UI组件库**: Element Plus
- **HTTP客户端**: Axios
- **路由**: Vue Router

### 客户端

- **语言**: Python 3.x
- **HTTP客户端**: requests, aiohttp
- **图像处理**: OpenCV
- **并发处理**: asyncio

## 项目结构

```
d:\codde\python\-YOLOv11-\
├── backend\
│   ├── springboot\
│   │   ├── src\
│   │   │   ├── main\
│   │   │   │   ├── java\
│   │   │   │   │   └── com\
│   │   │   │   │       └── yolo\
│   │   │   │   │           └── drone\
│   │   │   │   │               ├── controller\
│   │   │   │   │               │   ├── AuthController.java
│   │   │   │   │               ├── ApiController.java
│   │   │   │   │               ├── interceptor\
│   │   │   │   │               │   ├── TokenInterceptor.java
│   │   │   │   │               │   ├── WebMvcConfig.java
│   │   │   │   │               ├── entity\
│   │   │   │   │               │   ├── User.java
│   │   │   │   │               │   ├── Drone.java
│   │   │   │   │               ├── repository\
│   │   │   │   │               │   ├── UserRepository.java
│   │   │   │   │               │   ├── DroneRepository.java
│   │   │   │   │               ├── service\
│   │   │   │   │               │   ├── UserService.java
│   │   │   │   │               │   ├── DroneService.java
│   │   │   │   │               ├── util\
│   │   │   │   │               │   └── TokenUtil.java
│   │   │   │   └── resources\
│   │   │   │       ├── application.properties
│   │   │   │       └── static\
│   │   │   └── pom.xml
│   ├── flask\
│   │   ├── app.py
│   │   ├── wsgi.py
│   │   ├── requirements.txt
│   │   └── static\
│   │       ├── drone_images\
│   │       │   └── drone_images\
│   │       │       ├── test_drone\
│   │       │       └── ...
│   │       └── drone_test_drone_yolo.jpg
│   └── frontend\
│       └── vue\
│           ├── src\
│           │   ├── api\
│           │   │   └── index.js
│           │   ├── views\
│           │   │   ├── Login.vue
│           │   │   ├── App.vue
│           │   │   └── Flying.vue
│           ├── index.html
│           ├── package.json
│           └── vite.config.js
├── drone_login_client.py
├── add_drone_via_api.py
└── README.md
```

## 功能模块

### 1. 用户认证模块

#### 1.1 用户注册

**接口**: `POST /api/register`

**请求参数**:
```json
{
  "userId": "string",
  "username": "string",
  "password": "string",
  "userRole": "string"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "userId": "string",
    "username": "string",
    "userRole": "string",
    "creationDate": "timestamp"
  }
}
```

**功能说明**:
- 创建新用户账号
- 支持用户ID、用户名、密码和角色
- 自动设置默认角色为"user"
- 检查用户名和用户ID是否已存在

#### 1.2 用户登录

**接口**: `POST /api/login`

**请求参数**:
```json
{
  "username": "string",
  "password": "string"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "token": "string",
    "userId": "string",
    "username": "string",
    "role": "string"
  }
}
```

**功能说明**:
- 验证用户名和密码
- 生成SHA256加密的token
- token格式: `{userId}:{username}:{role}:{timestamp}:{hash}`
- 返回用户信息和token

#### 1.3 Token验证

**实现方式**: 拦截器

**拦截规则**:
- 允许通过的接口: `/api/login`, `/api/register`, `/api/upload`
- 需要验证的接口: 其他所有接口

**验证逻辑**:
1. 从请求头或参数中获取token
2. 解析token获取用户信息
3. 验证token格式和时效性
4. 将用户信息存入request属性供后续使用

**Token格式**:
```
{userId}:{username}:{role}:{timestamp}:{hash}
```

**验证规则**:
- token格式必须正确
- token必须在有效时间内（24小时）
- SHA256哈希值必须匹配

### 2. 无人机管理模块

#### 2.1 无人机信息查询

**接口**: `POST /api/droneInfo`

**请求参数**:
```json
{
  "userId": "string"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "userId": "string",
    "status": "integer",
    "fromAddress": "string",
    "toAddress": "string",
    "completedTaskCount": "integer"
  }
}
```

**功能说明**:
- 根据用户ID查询无人机信息
- 返回无人机状态、起始位置、目标位置和完成任务数

#### 2.2 无人机信息创建

**接口**: `POST /api/createDrone`

**请求参数**:
```json
{
  "userId": "string",
  "status": "integer",
  "fromAddress": "string",
  "toAddress": "string",
  "completedTaskCount": "integer"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": 1
}
```

**功能说明**:
- 创建新的无人机记录
- 初始化无人机状态和位置信息
- 支持自定义起始位置和目标位置

#### 2.3 无人机信息更新

**接口**: `PUT /api/updateDrone`

**请求参数**:
```json
{
  "userId": "string",
  "status": "integer",
  "fromAddress": "string",
  "toAddress": "string",
  "completedTaskCount": "integer"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": 1
}
```

**功能说明**:
- 更新无人机信息
- 支持更新状态、位置和完成任务数

#### 2.4 所有无人机信息查询

**接口**: `POST /api/alldroneInfo`

**请求参数**: 无

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "userId": "string",
      "status": "integer",
      "fromAddress": "string",
      "toAddress": "string",
      "completedTaskCount": "integer"
    }
  ]
}
```

**功能说明**:
- 查询所有无人机信息
- 支持批量查询和状态过滤

### 3. 图片上传和检测模块

#### 3.1 图片上传

**接口**: `POST /api/upload`

**请求参数**:
```json
{
  "userId": "string",
  "image": "string (Base64编码)",
  "token": "string",
  "timestamp": "string (可选)"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "boxes": [
      {
        "class_name": "string",
        "confidence": "float",
        "xyxy": [float, float, float, float]
      }
    ],
    "image": "string (Base64编码)",
    "is_control": "boolean",
    "position": "string",
    "control": "string"
  }
}
```

**功能说明**:
- 接收Base64编码的图片
- 转发到Flask服务进行YOLO检测
- 返回检测结果和标注后的图片
- 支持时间戳记录
- 自动生成避障指令

#### 3.2 YOLO预测

**接口**: `POST /predict`

**请求参数**:
```json
{
  "userId": "string",
  "image": "string (Base64编码)",
  "token": "string"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "boxes": [
      {
        "class_name": "string",
        "confidence": "float",
        "xyxy": [float, float, float, float]
      }
    ],
    "image": "string (Base64编码)",
    "filename": "string"
  }
}
```

**功能说明**:
- 使用YOLOv11模型进行目标检测
- 支持多种目标类别（person, car, book等）
- 返回边界框坐标和置信度
- 在图片上绘制边界框和标签
- 保存处理后的图片到文件系统

**检测类别**:
- person: 人员
- car: 汽车
- book: 书籍
- cell phone: 手机
- laptop: 笔记本电脑
- 其他类别根据模型训练结果

### 4. 图片历史和视频流模块

#### 4.1 获取最新图片

**接口**: `GET /flask/latest_image/<user_id>`

**响应**: 图片文件（JPEG格式）

**功能说明**:
- 优先从内存缓存返回最新图片
- 缓存未命中时从文件系统读取
- 支持多用户并发访问
- 自动更新缓存

**缓存机制**:
- 使用字典缓存最新图片
- 缓存大小限制：MAX_CACHE_SIZE
- 自动清理过期缓存

#### 4.2 获取图片历史

**接口**: `GET /flask/get_image_history`

**请求参数**:
```
userId: string
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "images": [
      "filename1.jpg",
      "filename2.jpg",
      ...
    ]
  }
}
```

**功能说明**:
- 返回指定用户的所有图片文件名
- 按修改时间排序（最新的在前）
- 支持分页查询（可扩展）

#### 4.3 删除图片

**接口**: `POST /flask/delete_image`

**请求参数**:
```json
{
  "userId": "string",
  "filename": "string"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": 1
}
```

**功能说明**:
- 删除指定图片文件
- 同时清理缓存
- 支持批量删除（可扩展）

#### 4.4 视频流模式

**前端实现**:
- 定时轮询获取最新图片
- 自动刷新显示
- 显示实时状态和延迟信息
- 支持手动启停

**更新频率**: 50ms（可配置）

**性能优化**:
- 使用Blob URL减少内存占用
- 避免重复加载
- 异步更新机制

### 5. 用户管理模块

#### 5.1 用户信息查询

**接口**: `POST /api/userInfo`

**请求参数**: 无

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "userId": "string",
      "username": "string",
      "userRole": "string",
      "creationDate": "timestamp"
    }
  ]
}
```

**功能说明**:
- 查询所有用户信息
- 支持分页查询（可扩展）
- 返回用户创建时间

#### 5.2 用户删除

**接口**: `DELETE /api/deleteUser`

**请求参数**:
```json
{
  "userId": "string"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": 1
}
```

**功能说明**:
- 根据用户ID删除用户
- 级联删除相关数据（可扩展）

#### 5.3 用户更新

**接口**: `PUT /api/updateUser`

**请求参数**:
```json
{
  "userId": "string",
  "username": "string",
  "password": "string",
  "userRole": "string"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": 1
}
```

**功能说明**:
- 更新用户信息
- 支持更新用户名、密码和角色
- 密码明文存储（可改进为加密）

#### 5.4 用户创建

**接口**: `POST /api/createUser`

**请求参数**:
```json
{
  "userId": "string",
  "username": "string",
  "password": "string",
  "userRole": "string"
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": 1
}
```

**功能说明**:
- 创建新用户
- 支持自定义角色
- 自动设置创建时间

## 数据库设计

### 表结构

#### user表

```sql
CREATE TABLE user (
  user_id VARCHAR(255) PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  user_role VARCHAR(50) DEFAULT 'user',
  creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**字段说明**:
- `user_id`: 用户唯一标识符
- `username`: 用户名，唯一约束
- `password`: 密码（明文存储，建议加密）
- `user_role`: 用户角色（user, admin, drone等）
- `creation_date`: 创建时间

#### drone表

```sql
CREATE TABLE drone (
  user_id VARCHAR(255) PRIMARY KEY,
  status INT DEFAULT 1,
  from_address VARCHAR(255),
  to_address VARCHAR(255),
  completed_task_count INT DEFAULT 0
);
```

**字段说明**:
- `user_id`: 用户ID，外键关联user表
- `status`: 无人机状态（1=飞行中，2=待命，3=维护中等）
- `from_address`: 起始位置
- `to_address`: 目标位置
- `completed_task_count`: 完成任务数

### 数据关系

```
user (1) ----< (N) ---- drone (N)
              |
              user_id (PK)
```

**关系说明**:
- user和drone是一对一关系
- user_id作为外键关联
- 支持多用户多无人机场景

## 部署指南

### 环境要求

#### 软件环境
- **Java**: JDK 17+
- **Python**: Python 3.8+
- **Node.js**: 16+
- **MySQL**: 8.0+
- **Maven**: 3.6+

#### Python依赖
```bash
pip install flask waitress opencv-python-headless pillow numpy ultralytics
```

#### Node.js依赖
```bash
npm install
```

### 启动顺序

1. **启动MySQL数据库**
```bash
# Windows
net start mysql80

# Linux
sudo systemctl start mysql
```

2. **启动Flask YOLO服务**
```bash
cd backend/flask
waitress-serve --listen=0.0.0.0:5001 --threads=10 wsgi:app
```

**配置说明**:
- 监听端口: 5001
- 线程数: 10
- 支持并发处理

3. **启动Spring Boot后端**
```bash
cd backend/springboot
mvn spring-boot:run
```

**配置说明**:
- 监听端口: 8080
- 数据库连接: localhost:3306
- 自动创建和更新表结构

4. **启动Vue前端**
```bash
cd frontend/vue
npm run dev
```

**配置说明**:
- 开发服务器端口: 5173
- 代理配置: /api → http://localhost:8080, /flask → http://localhost:5001
- 热重载支持

### 生产环境部署

#### Nginx配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /flask {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

#### Docker部署（可选）

**docker-compose.yml**:
```yaml
version: '3'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root123456
      MYSQL_DATABASE: yolo
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  springboot:
    build: ./backend/springboot
    ports:
      - "8080:8080"
    depends_on:
      - mysql
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/yolo
      SPRING_DATASOURCE_USERNAME: root
      SPRING_DATASOURCE_PASSWORD: root123456

  flask:
    build: ./backend/flask
    ports:
      - "5001:5001"
    volumes:
      - ./backend/flask/static:/app/static
    depends_on:
      - springboot

  frontend:
    build: ./frontend/vue
    ports:
      - "80:80"
    depends_on:
      - springboot
      - flask
```

## 开发指南

### 前端开发

#### 环境配置

1. **安装依赖**
```bash
cd frontend/vue
npm install
```

2. **启动开发服务器**
```bash
npm run dev
```

3. **访问地址**
```
http://localhost:5173
```

#### 开发注意事项

- 使用Vue DevTools进行调试
- 修改vite.config.js中的代理配置需重启开发服务器
- API请求会自动添加token到请求头
- 路由守卫会自动检查登录状态

#### 常见开发任务

1. **添加新页面**
```bash
# 创建页面组件
cd frontend/vue/src/views
# 在frontend/vue/src/router/index.js中添加路由
```

2. **添加新API**
```javascript
// 在frontend/vue/src/api/index.js中添加
export const newApi = {
  newMethod(data) {
    return api.post('/newEndpoint', data)
  }
}
```

3. **修改样式**
```css
/* 在组件的<style>标签中添加样式 */
.custom-style {
  /* 样式定义 */
}
```

### 后端开发

#### Spring Boot开发

1. **项目结构**
```
src/main/java/com/yolo/drone/
├── controller/     # 控制器层
├── service/        # 服务层
├── repository/     # 数据访问层
├── entity/         # 实体层
├── util/           # 工具类
└── interceptor/    # 拦截器
```

2. **添加新接口**

**步骤1**: 创建实体类
```java
package com.yolo.drone.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

@Entity
@Table(name = "table_name")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class EntityName {
    @Id
    @Column(name = "column_name")
    private String fieldName;
    
    // 其他字段...
}
```

**步骤2**: 创建Repository
```java
package com.yolo.drone.repository;

import com.yolo.drone.entity.EntityName;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EntityNameRepository extends JpaRepository<EntityName, String> {
    // 自定义查询方法
}
```

**步骤3**: 创建Service
```java
package com.yolo.drone.service;

import com.yolo.drone.entity.EntityName;
import com.yolo.drone.repository.EntityNameRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class EntityNameService {
    @Autowired
    private EntityNameRepository repository;
    
    public List<EntityName> findAll() {
        return repository.findAll();
    }
    
    public Optional<EntityName> findById(String id) {
        return repository.findById(id);
    }
    
    public EntityName save(EntityName entity) {
        return repository.save(entity);
    }
    
    public void deleteById(String id) {
        repository.deleteById(id);
    }
}
```

**步骤4**: 创建Controller
```java
package com.yolo.drone.controller;

import com.yolo.drone.entity.EntityName;
import com.yolo.drone.service.EntityNameService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class EntityNameController {
    @Autowired
    private EntityNameService service;
    
    @PostMapping("/endpoint")
    public ResponseEntity<?> endpoint(@RequestBody Map<String, Object> payload) {
        try {
            // 业务逻辑
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "message", "success",
                "data", result
            ));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "code", 500,
                "message", e.getMessage()
            ));
        }
    }
}
```

**步骤5**: 配置拦截器
```java
package com.yolo.drone.interceptor;

import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Component
public class CustomInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        // 拦截逻辑
        return true;
    }
}

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {
    @Autowired
    private CustomInterceptor customInterceptor;
    
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(customInterceptor)
                .addPathPatterns("/**")
                .excludePathPatterns("/api/login", "/api/register");
    }
}
```

#### Flask开发

1. **项目结构**
```
backend/flask/
├── app.py              # 主应用文件
├── wsgi.py             # WSGI配置
├── requirements.txt      # 依赖列表
└── static/             # 静态文件目录
    └── drone_images/  # 图片存储目录
```

2. **添加新接口**

```python
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route('/new_endpoint', methods=['POST'])
def new_endpoint():
    data = request.get_json()
    # 业务逻辑
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': result
    })

@app.route('/serve_image/<user_id>/<filename>', methods=['GET'])
def serve_image(user_id, filename):
    # 返回图片文件
    return send_from_directory('static/drone_images', filename)
```

3. **配置说明**

**app.py配置**:
- 静态文件目录: `./static`
- 图片保存目录: `./static/drone_images/`
- 支持跨域请求（生产环境需要配置）

**wsgi.py配置**:
```python
from app import app

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5001)
```

### 无人机客户端开发

#### 客户端架构

```
DroneLoginClient
├── login()              # 登录方法
├── capture_from_camera()  # 摄像头捕获
├── send_image()         # 发送图片
├── start_continuous_send()  # 启动持续发送
├── stop_continuous_send()  # 停止持续发送
└── receive_command()    # 接收指令
```

#### 核心功能

1. **登录认证**
```python
def login(self):
    response = requests.post(f"{self.base_url}/login", json={
        'username': self.username,
        'password': self.password
    })
    
    if response.status_code == 200:
        result = response.json()
        if result.get("code") == 200:
            self.token = result.get("data", {}).get("token")
            self.logged_in = True
            return True
    return False
```

2. **图片捕获**
```python
def capture_from_camera(self):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        _, img_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        return img_base64
    cap.release()
```

3. **异步发送**
```python
async def async_send_image(self, image_base64, session):
    payload = {
        "userId": self.drone_id,
        "image": f"data:image/jpeg;base64,{image_base64}",
        "token": self.token
    }
    
    async with session.post(f"{self.base_url}/upload", json=payload) as response:
        result = await response.json()
        if result.get("code") == 200:
            self.receive_command(result.get("data", {}))
```

4. **多线程处理**
```python
def start_continuous_send(self):
    self.running = True
    
    # 捕获线程
    self.capture_thread = threading.Thread(target=self.capture_images)
    self.capture_thread.start()
    
    # 发送线程
    self.send_thread = threading.Thread(target=self.send_images)
    self.send_thread.start()
```

## 常见问题

### 前端问题

#### 1. 跨域问题

**问题**: API请求被CORS阻止

**解决方案**:
- 确保后端配置了CORS
- 检查vite.config.js中的代理配置
- 使用正确的请求头

#### 2. Token过期问题

**问题**: Token过期后无法访问API

**解决方案**:
- Token有效期设置为24小时
- 前端检测到401错误时自动跳转登录页
- 提示用户重新登录

#### 3. 图片显示问题

**问题**: 前端无法显示无人机图片

**解决方案**:
- 确保URL参数正确传递userId
- 检查Flask服务的latest_image接口是否正常
- 查看浏览器控制台的网络请求日志
- 确认vite.config.js中没有rewrite规则影响URL路由

#### 4. 视频流延迟问题

**问题**: 视频流更新延迟过高

**解决方案**:
- 调整imageLoadInterval参数（当前50ms）
- 优化Flask服务的缓存机制
- 使用Blob URL减少内存占用
- 检查网络连接质量

### 后端问题

#### 1. 数据库连接问题

**问题**: 无法连接到MySQL数据库

**解决方案**:
- 检查MySQL服务是否启动
- 确认application.properties中的数据库配置
- 检查用户名和密码是否正确
- 查看防火墙设置

#### 2. Flask服务问题

**问题**: Flask服务无法启动或崩溃

**解决方案**:
- 检查Python依赖是否安装完整
- 检查YOLO模型文件是否存在
- 查看端口5001是否被占用
- 检查waitress配置是否正确

#### 3. Spring Boot问题

**问题**: Spring Boot启动失败

**解决方案**:
- 检查JDK版本是否正确（需要17+）
- 检查Maven配置是否正确
- 清理Maven缓存: `mvn clean`
- 检查pom.xml中的依赖版本冲突
- 查看application.properties配置

### 客户端问题

#### 1. 摄像头访问问题

**问题**: 无法访问摄像头

**解决方案**:
- 检查摄像头权限设置
- 关闭其他占用摄像头的程序
- 尝试使用不同的摄像头索引
- 检查OpenCV是否正确安装

#### 2. 网络连接问题

**问题**: 无法连接到服务器

**解决方案**:
- 检查服务器地址和端口是否正确
- 检查网络连接
- 检查防火墙设置
- 使用ping命令测试连接

#### 3. 图片发送失败

**问题**: 图片发送失败或超时

**解决方案**:
- 检查token是否有效
- 检查网络连接质量
- 调整图片质量和大小
- 增加重试机制

## 性能优化建议

### 前端优化

1. **代码分割**
   - 使用路由懒加载
   - 按需加载组件分割代码
   - 使用Tree Shaking减少包体积

2. **资源优化**
   - 图片懒加载
   - 使用CDN加速静态资源
   - 启用Gzip压缩

3. **请求优化**
   - 合并多个API请求
   - 使用防抖和节流
   - 减少不必要的轮询

### 后端优化

1. **数据库优化**
   - 添加适当的索引
   - 使用连接池
   - 优化SQL查询
   - 使用缓存机制

2. **API优化**
   - 使用异步处理
   - 实现请求限流
   - 添加API版本控制
   - 优化JSON序列化

3. **Flask优化**
   - 使用多线程处理
   - 实现图片缓存
   - 优化YOLO推理速度
   - 使用批量处理

### 系统优化

1. **监控**
   - 添加性能监控
   - 实现日志记录
   - 设置告警机制
   - 定期检查系统健康状态

2. **扩展性**
   - 使用负载均衡
   - 实现水平扩展
   - 考虑使用消息队列
   - 优化数据库连接池

## 安全建议

### 认证安全

1. **Token安全**
   - 使用HTTPS传输（生产环境）
   - Token设置合理的过期时间
   - 实现Token刷新机制
   - 避免Token在URL中传递

2. **密码安全**
   - 使用bcrypt或Argon2加密存储密码
   - 实现密码强度检查
   - 强制密码复杂度要求
   - 定期提醒用户修改密码

3. **API安全**
   - 实现请求签名验证
   - 添加API限流
   - 防止SQL注入
   - 验证输入参数

### 数据安全

1. **备份策略**
   - 定期备份数据库
   - 实现增量备份
   - 测试备份恢复流程
   - 备份文件加密存储

2. **数据保护**
   - 实现数据加密
   - 访问控制
   - 审计日志记录
   - 敏感数据脱敏

## 测试指南

### 单元测试

#### Spring Boot测试

```java
@SpringBootTest
@AutoConfigureMockMvc
public class ControllerTest {
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    public void testLogin() throws Exception {
        mockMvc.perform(post("/api/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"username\":\"test\",\"password\":\"123456\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }
}
```

#### Flask测试

```python
import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_predict(self):
        response = self.app.post('/predict', json={
            'userId': 'test',
            'image': 'base64_image_data',
            'token': 'test_token'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('boxes', response.json['data'])
```

#### 前端测试

```javascript
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'

describe('API', () => {
    it('should login successfully', async () => {
        const response = await authApi.login({
            username: 'test',
            password: '123456'
        })
        expect(response.data.code).toBe(200)
        expect(response.data.data).toHaveProperty('token')
    })
})
```

### 集成测试

1. **API集成测试**
   - 测试完整的用户流程
   - 测试图片上传和检测流程
   - 测试视频流功能
   - 验证错误处理

2. **端到端测试**
   - 测试前后端集成
   - 测试网络连接
   - 测试并发场景
   - 性能测试

## 维护指南

### 日常维护

1. **日志监控**
   - 定期检查应用日志
   - 监控错误日志
   - 分析性能指标
   - 设置告警阈值

2. **性能监控**
   - 监控API响应时间
   - 监控数据库查询性能
   - 监控YOLO推理速度
   - 优化慢查询

3. **资源监控**
   - 监控CPU使用率
   - 监控内存使用率
   - 监控磁盘空间
   - 监控网络带宽

### 版本升级

1. **依赖升级**
   - 定期更新依赖包
   - 检查安全漏洞
   - 测试兼容性
   - 备份当前版本

2. **功能升级**
   - 评估新功能需求
   - 设计升级方案
   - 测试升级流程
   - 发布更新说明

### 故障处理

1. **常见故障**
   - 服务无法启动
   - 数据库连接失败
   - API响应超时
   - 内存溢出
   - 磁盘空间不足

2. **故障排查流程**
   - 查看日志文件
   - 检查系统资源
   - 重启相关服务
   - 回滚到上一个稳定版本

3. **应急预案**
   - 准备回滚方案
   - 准备数据恢复方案
   - 准备服务切换方案
   - 定期演练应急流程

## 附录

### 配置文件说明

#### Spring Boot配置

```properties
# application.properties
spring.application.name=drone-system
server.port=8080
spring.datasource.url=jdbc:mysql://localhost:3306/yolo?useSSL=false&serverTimezone=UTC&allowPublicKeyRetrieval=true&createDatabaseIfNotExist=true
spring.datasource.username=root
spring.datasource.password=123456
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
flask.service.url=http://localhost:5001/predict
```

#### Flask配置

```python
# config.py (可选)
import os

class Config:
    SECRET_KEY = 'your-secret-key-here'
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    IMAGE_SAVE_DIR = './static/drone_images'
    MAX_CACHE_SIZE = 100
    YOLO_MODEL_PATH = './models/yolo11n.pt'
```

#### 前端配置

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      },
      '/flask': {
        target: 'http://localhost:5001',
        changeOrigin: true
      }
    }
  }
})
```

### 环境变量

```bash
# .env文件
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_DATABASE=yolo

SPRING_BOOT_PORT=8080
FLASK_PORT=5001
VITE_PORT=5173

JWT_SECRET=your-jwt-secret-key
TOKEN_EXPIRE_HOURS=24
```

### 端口占用

| 服务 | 端口 | 说明 |
|------|------|------|
| MySQL | 3306 | 数据库端口 |
| Spring Boot | 8080 | 后端API端口 |
| Flask | 5001 | YOLO服务端口 |
| Vue Dev | 5173 | 前端开发端口 |

## 联系和支持

### 开发团队

- **项目负责人**: [姓名]
- **后端开发**: [姓名]
- **前端开发**: [姓名]
- **AI算法**: [姓名]
- **运维支持**: [姓名]

### 技术支持

- **Spring Boot文档**: https://spring.io/projects/spring-boot
- **Vue文档**: https://vuejs.org/
- **Flask文档**: https://flask.palletsprojects.com/
- **YOLO文档**: https://docs.ultralytics.com/
- **MySQL文档**: https://dev.mysql.com/doc/

### 许可证

本项目采用MIT许可证，允许自由使用、修改和分发。

## 更新日志

### 版本历史

- **v1.0.0** (2026-01-19): 初始版本
  - 实现基本的用户认证
  - 实现YOLO障碍物检测
  - 实现前端监控界面
  - 实现无人机客户端

### 未来计划

- **v1.1.0**: 增强功能
  - 添加WebSocket实时通信
  - 实现多无人机管理
  - 优化YOLO推理性能
  - 添加数据分析功能
  - 实现移动端支持

- **v1.2.0**: 企业级功能
  - 添加权限管理系统
  - 实现审计日志
  - 优化系统性能
  - 添加监控告警
  - 实现自动化部署

---

**文档版本**: v1.0.0  
**最后更新**: 2026-01-19  
**维护者**: 开发团队
