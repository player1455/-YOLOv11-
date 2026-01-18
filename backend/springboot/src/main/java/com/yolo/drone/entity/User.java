package com.yolo.drone.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Entity
@Table(name = "user")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    
    @Column(name = "username", nullable = false)
    private String username;
    
    @Id
    @Column(name = "user_id", nullable = false)
    private String userId;
    
    @Column(name = "user_role", nullable = false)
    private String userRole;
    
    @Column(name = "creation_date")
    private LocalDateTime creationDate;
    
    @PrePersist
    protected void onCreate() {
        creationDate = LocalDateTime.now();
    }
}
