package com.yolo.drone.service;

import com.yolo.drone.constant.DroneStatus;
import com.yolo.drone.entity.Drone;
import com.yolo.drone.exception.BusinessException;
import com.yolo.drone.repository.DroneRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class DroneService {
    private static final Logger logger = LoggerFactory.getLogger(DroneService.class);

    @Autowired
    private DroneRepository droneRepository;

    public List<Drone> getAllDrones() {
        logger.info("获取所有无人机列表");
        return droneRepository.findAll();
    }

    public Optional<Drone> getDroneById(String userId) {
        logger.info("根据ID获取无人机: {}", userId);
        return droneRepository.findById(userId);
    }

    public List<Drone> getDronesByStatus(Integer status) {
        logger.info("根据状态获取无人机列表: {}", status);
        return droneRepository.findByStatus(status);
    }

    public List<Drone> getDronesByDestination(String toAddress) {
        logger.info("根据目的地获取无人机列表: {}", toAddress);
        return droneRepository.findByToAddress(toAddress);
    }

    public Drone createDrone(Drone drone) {
        logger.info("创建无人机: {}", drone.getUserId());
        if (droneRepository.existsById(drone.getUserId())) {
            throw new BusinessException("无人机已存在: " + drone.getUserId());
        }
        if (drone.getStatus() == null) {
            drone.setStatus(DroneStatus.STANDBY);
        }
        if (drone.getCompletedTaskCount() == null) {
            drone.setCompletedTaskCount(0);
        }
        return droneRepository.save(drone);
    }

    public Drone updateDrone(Drone drone) {
        logger.info("更新无人机: {}", drone.getUserId());
        if (!droneRepository.existsById(drone.getUserId())) {
            throw new BusinessException("无人机不存在: " + drone.getUserId());
        }
        return droneRepository.save(drone);
    }

    public void deleteDrone(String userId) {
        logger.info("删除无人机: {}", userId);
        if (!droneRepository.existsById(userId)) {
            throw new BusinessException("无人机不存在: " + userId);
        }
        droneRepository.deleteById(userId);
    }

    public void updateDroneStatus(String userId, Integer status) {
        logger.info("更新无人机状态: {} -> {}", userId, status);
        Optional<Drone> droneOptional = droneRepository.findById(userId);
        if (droneOptional.isEmpty()) {
            throw new BusinessException("无人机不存在: " + userId);
        }
        Drone drone = droneOptional.get();
        drone.setStatus(status);
        droneRepository.save(drone);
    }

    public void incrementTaskCount(String userId) {
        logger.info("增加无人机任务计数: {}", userId);
        Optional<Drone> droneOptional = droneRepository.findById(userId);
        if (droneOptional.isEmpty()) {
            throw new BusinessException("无人机不存在: " + userId);
        }
        Drone drone = droneOptional.get();
        drone.setCompletedTaskCount((drone.getCompletedTaskCount() != null ? drone.getCompletedTaskCount() : 0) + 1);
        droneRepository.save(drone);
    }
}
