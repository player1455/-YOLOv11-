package com.yolo.drone.interceptor;

import com.yolo.drone.util.TokenUtil;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Map;

@Component
public class TokenInterceptor implements HandlerInterceptor {
    private static final Logger logger = LoggerFactory.getLogger(TokenInterceptor.class);
    
    @Autowired
    private TokenUtil tokenUtil;
    
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        String requestURI = request.getRequestURI();
        logger.info("Request URI: " + requestURI);
        
        if (requestURI.contains("/login") || requestURI.contains("/register") || 
            requestURI.contains("/upload") || requestURI.contains("/alldroneInfo") ||
            requestURI.contains("/userInfo") || requestURI.contains("/createUser") ||
            requestURI.contains("/updateUser") || requestURI.contains("/deleteUser") ||
            requestURI.contains("/createDrone") || requestURI.contains("/updateDrone") ||
            requestURI.contains("/getLatestPrediction")) {
            return true;
        }
        
        String token = request.getHeader("Authorization");
        if (token == null || token.isEmpty()) {
            token = request.getParameter("token");
        }
        
        if (token == null || token.isEmpty() || !tokenUtil.validateToken(token)) {
            response.setContentType("application/json;charset=UTF-8");
            PrintWriter writer = response.getWriter();
            Map<String, Object> result = new HashMap<>();
            result.put("code", 401);
            result.put("message", "无效的token");
            result.put("data", null);
            writer.write(new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(result));
            writer.flush();
            writer.close();
            return false;
        }
        
        Map<String, String> userInfo = tokenUtil.parseToken(token);
        if (userInfo == null) {
            response.setContentType("application/json;charset=UTF-8");
            PrintWriter writer = response.getWriter();
            Map<String, Object> result = new HashMap<>();
            result.put("code", 401);
            result.put("message", "无效的token");
            result.put("data", null);
            writer.write(new com.fasterxml.jackson.databind.ObjectMapper().writeValueAsString(result));
            writer.flush();
            writer.close();
            return false;
        }
        
        request.setAttribute("userId", userInfo.get("userId"));
        request.setAttribute("username", userInfo.get("username"));
        request.setAttribute("role", userInfo.get("role"));
        
        return true;
    }
}
