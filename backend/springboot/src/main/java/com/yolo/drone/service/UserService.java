package com.yolo.drone.service;

import com.yolo.drone.constant.UserRole;
import com.yolo.drone.dto.LoginRequest;
import com.yolo.drone.dto.LoginResponse;
import com.yolo.drone.dto.RegisterRequest;
import com.yolo.drone.entity.User;
import com.yolo.drone.exception.AuthenticationException;
import com.yolo.drone.exception.BusinessException;
import com.yolo.drone.repository.UserRepository;
import com.yolo.drone.util.TokenUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class UserService {
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private TokenUtil tokenUtil;

    public List<User> getAllUsers() {
        logger.info("获取所有用户列表");
        return userRepository.findAll();
    }

    public Optional<User> getUserById(String userId) {
        logger.info("根据ID获取用户: {}", userId);
        return userRepository.findById(userId);
    }

    public Optional<User> getUserByUsername(String username) {
        logger.info("根据用户名获取用户: {}", username);
        return userRepository.findByUsername(username);
    }

    public List<User> getUsersByRole(String role) {
        logger.info("根据角色获取用户列表: {}", role);
        return userRepository.findByUserRole(role);
    }

    public User createUser(User user) {
        logger.info("创建用户: {}", user.getUserId());
        if (existsByUsername(user.getUsername())) {
            throw new BusinessException("用户名已存在: " + user.getUsername());
        }
        if (existsByUserId(user.getUserId())) {
            throw new BusinessException("用户ID已存在: " + user.getUserId());
        }
        if (user.getCreationDate() == null) {
            user.setCreationDate(LocalDateTime.now());
        }
        if (user.getUserRole() == null) {
            user.setUserRole(UserRole.USER);
        }
        return userRepository.save(user);
    }

    public User registerUser(RegisterRequest request) {
        logger.info("注册用户: {}", request.getUsername());
        if (existsByUsername(request.getUsername())) {
            throw new BusinessException("用户名已存在: " + request.getUsername());
        }
        if (existsByUserId(request.getUserId())) {
            throw new BusinessException("用户ID已存在: " + request.getUserId());
        }

        User user = new User();
        user.setUserId(request.getUserId());
        user.setUsername(request.getUsername());
        user.setPassword(request.getPassword());
        user.setUserRole(request.getUserRole() != null ? request.getUserRole() : UserRole.USER);
        user.setCreationDate(LocalDateTime.now());

        return userRepository.save(user);
    }

    public LoginResponse login(LoginRequest request) {
        logger.info("用户登录: {}", request.getUsername());
        Optional<User> userOptional = userRepository.findByUsername(request.getUsername());
        
        if (userOptional.isEmpty()) {
            throw new AuthenticationException("用户名或密码错误");
        }

        User user = userOptional.get();
        if (!user.getPassword().equals(request.getPassword())) {
            throw new AuthenticationException("用户名或密码错误");
        }

        String token = tokenUtil.generateToken(user.getUserId(), user.getUsername(), user.getUserRole());
        
        return new LoginResponse(token, user.getUserId(), user.getUsername(), user.getUserRole());
    }

    public User updateUser(User user) {
        logger.info("更新用户: {}", user.getUserId());
        if (!userRepository.existsById(user.getUserId())) {
            throw new BusinessException("用户不存在: " + user.getUserId());
        }
        return userRepository.save(user);
    }

    public void deleteUser(String userId) {
        logger.info("删除用户: {}", userId);
        if (!userRepository.existsById(userId)) {
            throw new BusinessException("用户不存在: " + userId);
        }
        userRepository.deleteById(userId);
    }

    public boolean existsByUsername(String username) {
        return userRepository.existsByUsername(username);
    }

    public boolean existsByUserId(String userId) {
        return userRepository.existsByUserId(userId);
    }

    public void validateToken(String token) {
        if (token == null || token.isEmpty()) {
            throw new AuthenticationException("Token不能为空");
        }
        if (!tokenUtil.validateToken(token)) {
            throw new AuthenticationException("Token无效或已过期");
        }
    }
}
