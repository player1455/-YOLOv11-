package com.yolo.drone.service;

import com.yolo.drone.entity.ControlLog;
import com.yolo.drone.repository.ControlLogRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ControlLogService {
    
    @Autowired
    private ControlLogRepository controlLogRepository;
    
    public List<ControlLog> getAllControlLogs() {
        return controlLogRepository.findAll();
    }
    
    public List<ControlLog> getControlLogsByUserId(String userId) {
        return controlLogRepository.findByUserId(userId);
    }
    
    public List<ControlLog> getControlLogsByOperationType(String operationType) {
        return controlLogRepository.findByOperationType(operationType);
    }
    
    public ControlLog createControlLog(ControlLog controlLog) {
        return controlLogRepository.save(controlLog);
    }
}
