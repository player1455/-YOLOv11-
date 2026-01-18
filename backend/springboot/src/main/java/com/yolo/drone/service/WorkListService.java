package com.yolo.drone.service;

import com.yolo.drone.entity.WorkList;
import com.yolo.drone.repository.WorkListRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class WorkListService {
    
    @Autowired
    private WorkListRepository workListRepository;
    
    public List<WorkList> getAllWorkLists() {
        return workListRepository.findAll();
    }
    
    public Optional<WorkList> getWorkListById(String taskId) {
        return workListRepository.findById(taskId);
    }
    
    public List<WorkList> getWorkListsByStatus(String status) {
        return workListRepository.findByStatus(status);
    }
    
    public List<WorkList> getWorkListsByDroneId(String droneId) {
        return workListRepository.findByAcceptedDroneId(droneId);
    }
    
    public WorkList createWorkList(WorkList workList) {
        return workListRepository.save(workList);
    }
    
    public WorkList updateWorkList(WorkList workList) {
        return workListRepository.save(workList);
    }
    
    public void deleteWorkList(String taskId) {
        workListRepository.deleteById(taskId);
    }
}
