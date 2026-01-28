package com.yolo.drone.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class YoloPredictResponse {
    private List<YoloBox> boxes;
    private String image;
    private String filename;
}
