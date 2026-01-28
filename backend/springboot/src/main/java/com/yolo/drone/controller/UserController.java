package com.yolo.drone.controller;

import com.yolo.drone.dto.ApiResponse;
import com.yolo.drone.entity.User;
import com.yolo.drone.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/user")
public class UserController {
    private static final Logger logger = LoggerFactory.getLogger(UserController.class);

    @Autowired
    private UserService userService;

    @GetMapping("/list")
    public ApiResponse<List<User>> getAllUsers() {
        logger.info("获取所有用户列表");
        List<User> users = userService.getAllUsers();
        return ApiResponse.success(users);
    }

    @GetMapping("/{userId}")
    public ApiResponse<User> getUserById(@PathVariable String userId) {
        logger.info("获取用户信息: userId={}", userId);
        User user = userService.getUserById(userId)
                .orElseThrow(() -> new RuntimeException("用户不存在"));
        return ApiResponse.success(user);
    }

    @GetMapping("/role/{role}")
    public ApiResponse<List<User>> getUsersByRole(@PathVariable String role) {
        logger.info("根据角色获取用户列表: role={}", role);
        List<User> users = userService.getUsersByRole(role);
        return ApiResponse.success(users);
    }

    @PostMapping("/create")
    public ApiResponse<User> createUser(@RequestBody User user) {
        logger.info("创建用户: userId={}", user.getUserId());
        User createdUser = userService.createUser(user);
        return ApiResponse.success(createdUser);
    }

    @PutMapping("/update")
    public ApiResponse<User> updateUser(@RequestBody User user) {
        logger.info("更新用户: userId={}", user.getUserId());
        User updatedUser = userService.updateUser(user);
        return ApiResponse.success(updatedUser);
    }

    @DeleteMapping("/{userId}")
    public ApiResponse<Void> deleteUser(@PathVariable String userId) {
        logger.info("删除用户: userId={}", userId);
        userService.deleteUser(userId);
        return ApiResponse.success(null);
    }
}
