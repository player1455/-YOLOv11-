package com.yolo.drone.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class YoloPredictRequest {
    private String userId;
    private String image;
    private String token;
    private String timestamp;
}
