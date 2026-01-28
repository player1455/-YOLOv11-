package com.yolo.drone.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class YoloBox {
    private String class_name;
    private Float confidence;
    private List<Float> xyxy;
}
