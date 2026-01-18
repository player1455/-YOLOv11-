package com.yolo.drone.repository;

import com.yolo.drone.entity.Drone;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface DroneRepository extends JpaRepository<Drone, String> {
    
    Optional<Drone> findByUserId(String userId);
    
    List<Drone> findByStatus(Integer status);
    
    List<Drone> findByToAddress(String toAddress);
}
