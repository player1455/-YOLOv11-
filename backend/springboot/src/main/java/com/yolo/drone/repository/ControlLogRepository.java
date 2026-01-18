package com.yolo.drone.repository;

import com.yolo.drone.entity.ControlLog;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ControlLogRepository extends JpaRepository<ControlLog, Integer> {
    
    List<ControlLog> findByUserId(String userId);
    
    List<ControlLog> findByOperationType(String operationType);
}
