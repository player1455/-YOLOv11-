package com.yolo.drone.controller;

import com.yolo.drone.dto.ApiResponse;
import com.yolo.drone.dto.UploadImageRequest;
import com.yolo.drone.dto.YoloBox;
import com.yolo.drone.dto.YoloPredictResponse;
import com.yolo.drone.entity.Drone;
import com.yolo.drone.entity.User;
import com.yolo.drone.service.DroneService;
import com.yolo.drone.service.UserService;
import com.yolo.drone.util.TokenUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class ApiController {
    private static final Logger logger = LoggerFactory.getLogger(ApiController.class);

    @Autowired
    private UserService userService;

    @Autowired
    private DroneService droneService;

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private TokenUtil tokenUtil;

    @Value("${flask.service.url}")
    private String flaskServiceUrl;

    @PostMapping("/upload")
    public ApiResponse<Map<String, Object>> uploadImage(@RequestBody UploadImageRequest request) {
        logger.info("上传图片请求: userId={}", request.getUserId());

        Map<String, Object> flaskRequest = new HashMap<>();
        flaskRequest.put("userId", request.getUserId());
        flaskRequest.put("image", request.getImage());
        flaskRequest.put("token", request.getToken());

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(flaskRequest, headers);

        ResponseEntity<Map> flaskResponse = restTemplate.postForEntity(flaskServiceUrl, entity, Map.class);

        Map<String, Object> responseData = new HashMap<>();
        if (flaskResponse.getBody() != null && flaskResponse.getBody().containsKey("data")) {
            Map<String, Object> flaskData = (Map<String, Object>) flaskResponse.getBody().get("data");
            responseData.put("boxes", flaskData.get("boxes"));
            responseData.put("is_control", false);
            responseData.put("position", "left");
            responseData.put("control", "right");
            responseData.put("image", flaskData.get("image"));
        }

        return ApiResponse.success(responseData);
    }

    @PostMapping("/droneInfo")
    public ApiResponse<Drone> getDroneInfo(@RequestBody Map<String, String> payload) {
        String userId = payload.get("userId");
        logger.info("获取无人机信息: userId={}", userId);

        Drone drone = droneService.getDroneById(userId)
                .orElseThrow(() -> new RuntimeException("无人机不存在"));

        return ApiResponse.success(drone);
    }

    @PostMapping("/alldroneInfo")
    public ApiResponse<List<Drone>> getAllDroneInfo() {
        logger.info("获取所有无人机信息");
        List<Drone> drones = droneService.getAllDrones();
        return ApiResponse.success(drones);
    }

    @PostMapping("/userInfo")
    public ApiResponse<List<User>> getUserInfo() {
        logger.info("获取所有用户信息");
        List<User> users = userService.getAllUsers();
        return ApiResponse.success(users);
    }

    @DeleteMapping("/deleteUser")
    public ApiResponse<Integer> deleteUser(@RequestBody Map<String, String> payload) {
        String userId = payload.get("userId");
        logger.info("删除用户: userId={}", userId);
        userService.deleteUser(userId);
        return ApiResponse.success(1);
    }

    @PutMapping("/updateUser")
    public ApiResponse<Integer> updateUser(@RequestBody User user) {
        logger.info("更新用户: userId={}", user.getUserId());
        userService.updateUser(user);
        return ApiResponse.success(1);
    }

    @PostMapping("/createUser")
    public ApiResponse<Integer> createUser(@RequestBody User user) {
        logger.info("创建用户: userId={}", user.getUserId());
        userService.createUser(user);
        return ApiResponse.success(1);
    }

    @PostMapping("/createDrone")
    public ApiResponse<Integer> createDrone(@RequestBody Drone drone) {
        logger.info("创建无人机: userId={}", drone.getUserId());
        droneService.createDrone(drone);
        return ApiResponse.success(1);
    }

    @PutMapping("/updateDrone")
    public ApiResponse<Integer> updateDrone(@RequestBody Drone drone) {
        logger.info("更新无人机: userId={}", drone.getUserId());
        droneService.updateDrone(drone);
        return ApiResponse.success(1);
    }

    @PostMapping("/getLatestPrediction")
    public ApiResponse<Map<String, Object>> getLatestPrediction(@RequestBody Map<String, String> payload) {
        String userId = payload.get("userId");
        logger.info("获取最新预测结果: userId={}", userId);

        Map<String, Object> responseData = new HashMap<>();
        responseData.put("droneId", userId);
        responseData.put("lastPredictionTime", System.currentTimeMillis());
        responseData.put("prediction", Map.of(
                "boxes", List.of(),
                "image", "",
                "is_control", false,
                "position", "left",
                "control", "right"
        ));

        return ApiResponse.success(responseData);
    }
}
