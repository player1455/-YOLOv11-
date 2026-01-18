package com.yolo.drone.service;

import com.yolo.drone.entity.Drone;
import com.yolo.drone.repository.DroneRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class DroneService {
    
    @Autowired
    private DroneRepository droneRepository;
    
    public List<Drone> getAllDrones() {
        return droneRepository.findAll();
    }
    
    public Optional<Drone> getDroneById(String userId) {
        return droneRepository.findById(userId);
    }
    
    public List<Drone> getDronesByStatus(Integer status) {
        return droneRepository.findByStatus(status);
    }
    
    public List<Drone> getDronesByDestination(String toAddress) {
        return droneRepository.findByToAddress(toAddress);
    }
    
    public Drone createDrone(Drone drone) {
        return droneRepository.save(drone);
    }
    
    public Drone updateDrone(Drone drone) {
        return droneRepository.save(drone);
    }
    
    public void deleteDrone(String userId) {
        droneRepository.deleteById(userId);
    }
}
