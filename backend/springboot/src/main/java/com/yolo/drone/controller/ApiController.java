package com.yolo.drone.controller;

import com.yolo.drone.entity.Drone;
import com.yolo.drone.entity.User;
import com.yolo.drone.service.DroneService;
import com.yolo.drone.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api")
public class ApiController {
    
    @Autowired
    private UserService userService;
    
    @Autowired
    private DroneService droneService;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Value("${flask.service.url}")
    private String flaskServiceUrl;
    
    @PostMapping("/upload")
    public ResponseEntity<?> uploadImage(@RequestBody Map<String, Object> payload) {
        try {
            String userId = (String) payload.get("userId");
            String image = (String) payload.get("image");
            String token = (String) payload.get("token");
            
            if (userId == null || image == null) {
                return ResponseEntity.badRequest().body(Map.of(
                    "code", 400,
                    "message", "userId and image are required"
                ));
            }
            
            Map<String, Object> flaskRequest = new HashMap<>();
            flaskRequest.put("userId", userId);
            flaskRequest.put("image", image);
            flaskRequest.put("token", token);
            
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
                // 添加YOLO处理后的图片到返回结果中
                responseData.put("image", flaskData.get("image"));
            }
            
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "message", "success",
                "data", responseData
            ));
            
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "code", 500,
                "message", e.getMessage()
            ));
        }
    }
    
    @PostMapping("/droneInfo")
    public ResponseEntity<?> getDroneInfo(@RequestBody Map<String, String> payload) {
        try {
            String userId = payload.get("userId");
            
            if (userId == null) {
                return ResponseEntity.badRequest().body(Map.of(
                    "code", 400,
                    "message", "userId is required"
                ));
            }
            
            Optional<Drone> droneOpt = droneService.getDroneById(userId);
            if (droneOpt.isEmpty()) {
                return ResponseEntity.ok(Map.of(
                    "code", 404,
                    "message", "Drone not found",
                    "data", null
                ));
            }
            
            Drone drone = droneOpt.get();
            Map<String, Object> data = new HashMap<>();
            data.put("userId", drone.getUserId());
            data.put("condition", drone.getStatus());
            data.put("fromAddress", drone.getFromAddress());
            data.put("toAddress", drone.getToAddress());
            
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "message", "success",
                "data", data
            ));
            
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "code", 500,
                "message", e.getMessage()
            ));
        }
    }
    
    @PostMapping("/alldroneInfo")
    public ResponseEntity<?> getAllDroneInfo(@RequestBody Map<String, String> payload) {
        try {
            List<Drone> drones = droneService.getAllDrones();
            
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "message", "success",
                "data", drones
            ));
            
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "code", 500,
                "message", e.getMessage()
            ));
        }
    }
    
    @PostMapping("/userInfo")
    public ResponseEntity<?> getUserInfo(@RequestBody Map<String, String> payload) {
        try {
            List<User> users = userService.getAllUsers();
            
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "message", "success",
                "data", users
            ));
            
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "code", 500,
                "message", e.getMessage()
            ));
        }
    }
    
    @DeleteMapping("/deleteUser")
    public ResponseEntity<?> deleteUser(@RequestBody Map<String, String> payload) {
        try {
            String userId = payload.get("userId");
            
            if (userId == null) {
                return ResponseEntity.badRequest().body(Map.of(
                    "code", 400,
                    "message", "userId is required"
                ));
            }
            
            userService.deleteUser(userId);
            
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "message", "success",
                "data", 1
            ));
            
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "code", 500,
                "message", e.getMessage()
            ));
        }
    }
    
    @PutMapping("/updateUser")
    public ResponseEntity<?> updateUser(@RequestBody User user) {
        try {
            User updatedUser = userService.updateUser(user);
            
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "message", "success",
                "data", 1
            ));
            
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "code", 500,
                "message", e.getMessage()
            ));
        }
    }
    
    @PostMapping("/createUser")
    public ResponseEntity<?> createUser(@RequestBody User user) {
        try {
            User createdUser = userService.createUser(user);
            
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "message", "success",
                "data", 1
            ));
            
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "code", 500,
                "message", e.getMessage()
            ));
        }
    }
    
    @PostMapping("/createDrone")
    public ResponseEntity<?> createDrone(@RequestBody Drone drone) {
        try {
            Drone createdDrone = droneService.createDrone(drone);
            
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "message", "success",
                "data", 1
            ));
            
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "code", 500,
                "message", e.getMessage()
            ));
        }
    }
    
    @PutMapping("/updateDrone")
    public ResponseEntity<?> updateDrone(@RequestBody Drone drone) {
        try {
            Drone updatedDrone = droneService.updateDrone(drone);
            
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "message", "success",
                "data", 1
            ));
            
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "code", 500,
                "message", e.getMessage()
            ));
        }
    }
    
    @PostMapping("/getLatestPrediction")
    public ResponseEntity<?> getLatestPrediction(@RequestBody Map<String, String> payload) {
        try {
            String userId = payload.get("userId");
            
            if (userId == null) {
                return ResponseEntity.badRequest().body(Map.of(
                    "code", 400,
                    "message", "userId is required"
                ));
            }
            
            // 这里应该从数据库或文件系统中获取最新的预测结果
            // 目前我们返回一个示例响应，实际项目中应该实现从文件读取的逻辑
            Map<String, Object> responseData = new HashMap<>();
            responseData.put("message", "success");
            responseData.put("data", Map.of(
                "droneId", userId,
                "lastPredictionTime", System.currentTimeMillis(),
                "prediction", Map.of(
                    "boxes", List.of(),
                    "image", "",
                    "is_control", false,
                    "position", "left",
                    "control", "right"
                )
            ));
            
            return ResponseEntity.ok(Map.of(
                "code", 200,
                "message", "success",
                "data", responseData
            ));
            
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(Map.of(
                "code", 500,
                "message", e.getMessage()
            ));
        }
    }
}
