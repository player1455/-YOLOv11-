package com.yolo.drone.service;

import com.yolo.drone.entity.ControlLog;
import com.yolo.drone.repository.ControlLogRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
@Transactional
public class ControlLogService {
    private static final Logger logger = LoggerFactory.getLogger(ControlLogService.class);

    @Autowired
    private ControlLogRepository controlLogRepository;

    public List<ControlLog> getAllControlLogs() {
        logger.info("获取所有控制日志");
        return controlLogRepository.findAll();
    }

    public List<ControlLog> getControlLogsByUserId(String userId) {
        logger.info("根据用户ID获取控制日志: {}", userId);
        return controlLogRepository.findByUserId(userId);
    }

    public List<ControlLog> getControlLogsByOperationType(String operationType) {
        logger.info("根据操作类型获取控制日志: {}", operationType);
        return controlLogRepository.findByOperationType(operationType);
    }

    public ControlLog createControlLog(ControlLog controlLog) {
        logger.info("创建控制日志: {} - {}", controlLog.getUserId(), controlLog.getOperationType());
        if (controlLog.getOperationTime() == null) {
            controlLog.setOperationTime(LocalDateTime.now());
        }
        return controlLogRepository.save(controlLog);
    }

    public ControlLog logOperation(String userId, String operationType, String operationDetails) {
        logger.info("记录操作: {} - {}", userId, operationType);
        ControlLog controlLog = new ControlLog();
        controlLog.setUserId(userId);
        controlLog.setOperationType(operationType);
        controlLog.setOperationDetails(operationDetails);
        controlLog.setOperationTime(LocalDateTime.now());
        return controlLogRepository.save(controlLog);
    }

    public void deleteControlLogsByUserId(String userId) {
        logger.info("删除用户控制日志: {}", userId);
        List<ControlLog> logs = controlLogRepository.findByUserId(userId);
        controlLogRepository.deleteAll(logs);
    }
}
