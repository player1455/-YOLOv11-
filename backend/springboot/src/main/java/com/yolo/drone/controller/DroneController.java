package com.yolo.drone.controller;

import com.yolo.drone.dto.ApiResponse;
import com.yolo.drone.entity.Drone;
import com.yolo.drone.service.DroneService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/drone")
public class DroneController {
    private static final Logger logger = LoggerFactory.getLogger(DroneController.class);

    @Autowired
    private DroneService droneService;

    @GetMapping("/list")
    public ApiResponse<List<Drone>> getAllDrones() {
        logger.info("获取所有无人机列表");
        List<Drone> drones = droneService.getAllDrones();
        return ApiResponse.success(drones);
    }

    @GetMapping("/{userId}")
    public ApiResponse<Drone> getDroneById(@PathVariable String userId) {
        logger.info("获取无人机信息: userId={}", userId);
        Drone drone = droneService.getDroneById(userId)
                .orElseThrow(() -> new RuntimeException("无人机不存在"));
        return ApiResponse.success(drone);
    }

    @GetMapping("/status/{status}")
    public ApiResponse<List<Drone>> getDronesByStatus(@PathVariable Integer status) {
        logger.info("根据状态获取无人机列表: status={}", status);
        List<Drone> drones = droneService.getDronesByStatus(status);
        return ApiResponse.success(drones);
    }

    @GetMapping("/destination/{toAddress}")
    public ApiResponse<List<Drone>> getDronesByDestination(@PathVariable String toAddress) {
        logger.info("根据目的地获取无人机列表: toAddress={}", toAddress);
        List<Drone> drones = droneService.getDronesByDestination(toAddress);
        return ApiResponse.success(drones);
    }

    @PostMapping("/create")
    public ApiResponse<Drone> createDrone(@RequestBody Drone drone) {
        logger.info("创建无人机: userId={}", drone.getUserId());
        Drone createdDrone = droneService.createDrone(drone);
        return ApiResponse.success(createdDrone);
    }

    @PutMapping("/update")
    public ApiResponse<Drone> updateDrone(@RequestBody Drone drone) {
        logger.info("更新无人机: userId={}", drone.getUserId());
        Drone updatedDrone = droneService.updateDrone(drone);
        return ApiResponse.success(updatedDrone);
    }

    @PutMapping("/status")
    public ApiResponse<Void> updateDroneStatus(@RequestBody Map<String, Object> payload) {
        String userId = (String) payload.get("userId");
        Integer status = (Integer) payload.get("status");
        logger.info("更新无人机状态: userId={}, status={}", userId, status);
        droneService.updateDroneStatus(userId, status);
        return ApiResponse.success(null);
    }

    @DeleteMapping("/{userId}")
    public ApiResponse<Void> deleteDrone(@PathVariable String userId) {
        logger.info("删除无人机: userId={}", userId);
        droneService.deleteDrone(userId);
        return ApiResponse.success(null);
    }
}
