package com.yolo.drone.repository;

import com.yolo.drone.entity.WorkList;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface WorkListRepository extends JpaRepository<WorkList, String> {
    
    Optional<WorkList> findByTaskId(String taskId);
    
    List<WorkList> findByStatus(String status);
    
    List<WorkList> findByAcceptedDroneId(String acceptedDroneId);
}
