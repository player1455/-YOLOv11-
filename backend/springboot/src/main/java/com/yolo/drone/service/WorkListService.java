package com.yolo.drone.service;

import com.yolo.drone.constant.TaskStatus;
import com.yolo.drone.entity.WorkList;
import com.yolo.drone.exception.BusinessException;
import com.yolo.drone.repository.WorkListRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@Transactional
public class WorkListService {
    private static final Logger logger = LoggerFactory.getLogger(WorkListService.class);

    @Autowired
    private WorkListRepository workListRepository;

    public List<WorkList> getAllWorkLists() {
        logger.info("获取所有任务列表");
        return workListRepository.findAll();
    }

    public Optional<WorkList> getWorkListById(String taskId) {
        logger.info("根据ID获取任务: {}", taskId);
        return workListRepository.findById(taskId);
    }

    public List<WorkList> getWorkListsByStatus(String status) {
        logger.info("根据状态获取任务列表: {}", status);
        return workListRepository.findByStatus(status);
    }

    public List<WorkList> getWorkListsByDroneId(String droneId) {
        logger.info("根据无人机ID获取任务列表: {}", droneId);
        return workListRepository.findByAcceptedDroneId(droneId);
    }

    public WorkList createWorkList(WorkList workList) {
        logger.info("创建任务: {}", workList.getTaskId());
        if (workListRepository.existsById(workList.getTaskId())) {
            throw new BusinessException("任务已存在: " + workList.getTaskId());
        }
        if (workList.getStatus() == null) {
            workList.setStatus(TaskStatus.PENDING);
        }
        if (workList.getPublishTime() == null) {
            workList.setPublishTime(LocalDateTime.now());
        }
        return workListRepository.save(workList);
    }

    public WorkList publishTask(String taskId, String taskName, String fromAddress, String toAddress) {
        logger.info("发布任务: {} - {}", taskId, taskName);
        WorkList workList = new WorkList();
        workList.setTaskId(taskId);
        workList.setTaskName(taskName);
        workList.setFromAddress(fromAddress);
        workList.setToAddress(toAddress);
        workList.setStatus(TaskStatus.PENDING);
        workList.setPublishTime(LocalDateTime.now());
        return workListRepository.save(workList);
    }

    public WorkList acceptTask(String taskId, String droneId) {
        logger.info("接受任务: {} by {}", taskId, droneId);
        Optional<WorkList> workListOptional = workListRepository.findById(taskId);
        if (workListOptional.isEmpty()) {
            throw new BusinessException("任务不存在: " + taskId);
        }
        WorkList workList = workListOptional.get();
        if (!TaskStatus.PENDING.equals(workList.getStatus())) {
            throw new BusinessException("任务状态不允许接受: " + workList.getStatus());
        }
        workList.setStatus(TaskStatus.ACCEPTED);
        workList.setAcceptedDroneId(droneId);
        workList.setAcceptTime(LocalDateTime.now());
        return workListRepository.save(workList);
    }

    public WorkList completeTask(String taskId) {
        logger.info("完成任务: {}", taskId);
        Optional<WorkList> workListOptional = workListRepository.findById(taskId);
        if (workListOptional.isEmpty()) {
            throw new BusinessException("任务不存在: " + taskId);
        }
        WorkList workList = workListOptional.get();
        if (!TaskStatus.ACCEPTED.equals(workList.getStatus())) {
            throw new BusinessException("任务状态不允许完成: " + workList.getStatus());
        }
        workList.setStatus(TaskStatus.COMPLETED);
        workList.setCompletionTime(LocalDateTime.now());
        return workListRepository.save(workList);
    }

    public WorkList cancelTask(String taskId) {
        logger.info("取消任务: {}", taskId);
        Optional<WorkList> workListOptional = workListRepository.findById(taskId);
        if (workListOptional.isEmpty()) {
            throw new BusinessException("任务不存在: " + taskId);
        }
        WorkList workList = workListOptional.get();
        if (TaskStatus.COMPLETED.equals(workList.getStatus())) {
            throw new BusinessException("已完成任务不能取消");
        }
        workList.setStatus(TaskStatus.CANCELLED);
        return workListRepository.save(workList);
    }

    public WorkList updateWorkList(WorkList workList) {
        logger.info("更新任务: {}", workList.getTaskId());
        if (!workListRepository.existsById(workList.getTaskId())) {
            throw new BusinessException("任务不存在: " + workList.getTaskId());
        }
        return workListRepository.save(workList);
    }

    public void deleteWorkList(String taskId) {
        logger.info("删除任务: {}", taskId);
        if (!workListRepository.existsById(taskId)) {
            throw new BusinessException("任务不存在: " + taskId);
        }
        workListRepository.deleteById(taskId);
    }
}
