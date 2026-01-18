package com.yolo.drone.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "work_list")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class WorkList {
    
    @Column(name = "task_name", nullable = false)
    private String taskName;
    
    @Id
    @Column(name = "task_id", nullable = false)
    private String taskId;
    
    @Column(name = "from_address")
    private String fromAddress;
    
    @Column(name = "to_address")
    private String toAddress;
    
    @Column(name = "status")
    private String status;
    
    @Column(name = "accepted_drone_id")
    private String acceptedDroneId;
    
    @Column(name = "publish_time")
    private LocalDateTime publishTime;
    
    @Column(name = "accept_time")
    private LocalDateTime acceptTime;
    
    @Column(name = "completion_time")
    private LocalDateTime completionTime;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "accepted_drone_id", insertable = false, updatable = false)
    private Drone drone;
}
