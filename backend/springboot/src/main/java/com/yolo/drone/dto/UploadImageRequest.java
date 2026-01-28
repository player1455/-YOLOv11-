package com.yolo.drone.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UploadImageRequest {
    private String userId;
    private String image;
    private String token;
    private String timestamp;
}
