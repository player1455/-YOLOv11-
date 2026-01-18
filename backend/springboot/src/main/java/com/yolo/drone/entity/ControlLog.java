package com.yolo.drone.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "control_log")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ControlLog {
    
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Id
    @Column(name = "log_id")
    private Integer logId;
    
    @Column(name = "user_id", nullable = false)
    private String userId;
    
    @Column(name = "operation_type", nullable = false)
    private String operationType;
    
    @Column(name = "operation_time")
    private LocalDateTime operationTime;
    
    @Column(name = "operation_details", columnDefinition = "TEXT")
    private String operationDetails;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", insertable = false, updatable = false)
    private User user;
    
    @PrePersist
    protected void onCreate() {
        operationTime = LocalDateTime.now();
    }
}
