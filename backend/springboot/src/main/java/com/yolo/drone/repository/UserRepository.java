package com.yolo.drone.repository;

import com.yolo.drone.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, String> {
    
    Optional<User> findByUsername(String username);
    
    List<User> findByUserRole(String userRole);
    
    boolean existsByUsername(String username);
    
    boolean existsByUserId(String userId);
}
