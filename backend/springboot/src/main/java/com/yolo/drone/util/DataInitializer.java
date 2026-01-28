package com.yolo.drone.util;

import com.yolo.drone.entity.User;
import com.yolo.drone.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class DataInitializer implements CommandLineRunner {
    
    @Autowired
    private UserRepository userRepository;
    
    @Override
    public void run(String... args) throws Exception {
        if (!userRepository.existsByUsername("test_drone")) {
            User testDrone = new User();
            testDrone.setUserId("test_drone");
            testDrone.setUsername("test_drone");
            testDrone.setPassword("123456");
            testDrone.setUserRole("drone");
            testDrone.setCreationDate(LocalDateTime.now());
            userRepository.save(testDrone);
            System.out.println("Created test_drone user");
        }
        
        if (!userRepository.existsByUsername("admin")) {
            User admin = new User();
            admin.setUserId("admin");
            admin.setUsername("admin");
            admin.setPassword("admin123");
            admin.setUserRole("admin");
            admin.setCreationDate(LocalDateTime.now());
            userRepository.save(admin);
            System.out.println("Created admin user");
        }
    }
}
