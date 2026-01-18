package com.yolo.drone.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class StaticResourceConfig implements WebMvcConfigurer {
    
    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        // 将项目根目录下的static目录配置为静态资源目录
        registry.addResourceHandler("/drone_*.jpg")
                .addResourceLocations("file:../../static/")
                .setCachePeriod(0); // 禁用缓存，确保前端能获取到最新图片
    }
}