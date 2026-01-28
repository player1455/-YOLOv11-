package com.yolo.drone.controller;

import com.yolo.drone.dto.ApiResponse;
import com.yolo.drone.dto.LoginRequest;
import com.yolo.drone.dto.LoginResponse;
import com.yolo.drone.dto.RegisterRequest;
import com.yolo.drone.entity.User;
import com.yolo.drone.service.UserService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
public class AuthController {
    private static final Logger logger = LoggerFactory.getLogger(AuthController.class);

    @Autowired
    private UserService userService;

    @PostMapping("/login")
    public ApiResponse<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        logger.info("登录请求: {}", request.getUsername());
        LoginResponse response = userService.login(request);
        return ApiResponse.success("登录成功", response);
    }

    @PostMapping("/register")
    public ApiResponse<User> register(@Valid @RequestBody RegisterRequest request) {
        logger.info("注册请求: {}", request.getUsername());
        User user = userService.registerUser(request);
        return ApiResponse.success("注册成功", user);
    }
}
