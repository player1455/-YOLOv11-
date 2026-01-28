package com.yolo.drone.util;

import org.springframework.stereotype.Component;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.Instant;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

@Component
public class TokenUtil {

    // 密钥，实际项目中应该从配置文件读取
    private static final String SECRET_KEY = "your-secret-key-here"; // 生产环境中应替换为强密钥

    /**
     * 生成token，使用SHA256加密
     * @param userId 用户ID
     * @param username 用户名
     * @param role 用户角色
     * @return token字符串
     */
    public String generateToken(String userId, String username, String role) {
        try {
            // 构建token信息，包含账号信息
            String timestamp = String.valueOf(Instant.now().getEpochSecond());
            String tokenContent = String.format("%s|%s|%s|%s", userId, username, role, timestamp);
            
            // 使用SHA256生成签名
            String signature = generateSignature(tokenContent);
            
            // 构建完整token
            String token = String.format("%s.%s", tokenContent, signature);
            
            // 使用Base64编码
            return Base64.getEncoder().encodeToString(token.getBytes());
        } catch (Exception e) {
            throw new RuntimeException("生成token失败", e);
        }
    }

    /**
     * 验证token是否有效
     * @param token token字符串
     * @return 验证结果
     */
    public boolean validateToken(String token) {
        try {
            // 解码Base64
            String decodedToken = new String(Base64.getDecoder().decode(token));
            
            // 分割token内容和签名
            int lastDotIndex = decodedToken.lastIndexOf('.');
            if (lastDotIndex == -1) {
                return false;
            }
            
            String tokenContent = decodedToken.substring(0, lastDotIndex);
            String signature = decodedToken.substring(lastDotIndex + 1);
            
            // 重新生成签名并验证
            String generatedSignature = generateSignature(tokenContent);
            return Objects.equals(signature, generatedSignature);
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * 从token中获取用户信息
     * @param token token字符串
     * @return 用户信息map
     */
    public Map<String, String> parseToken(String token) {
        try {
            // 解码Base64
            String decodedToken = new String(Base64.getDecoder().decode(token));
            
            // 分割token内容和签名
            int lastDotIndex = decodedToken.lastIndexOf('.');
            if (lastDotIndex == -1) {
                return null;
            }
            
            String tokenContent = decodedToken.substring(0, lastDotIndex);
            
            // 分割token内容
            String[] parts = tokenContent.split("\\|");
            if (parts.length != 4) {
                return null;
            }
            
            // 构建用户信息map
            Map<String, String> userInfo = new HashMap<>();
            userInfo.put("userId", parts[0]);
            userInfo.put("username", parts[1]);
            userInfo.put("role", parts[2]);
            userInfo.put("timestamp", parts[3]);
            
            return userInfo;
        } catch (Exception e) {
            return null;
        }
    }

    /**
     * 使用SHA256生成签名
     * @param content 待签名内容
     * @return 签名字符串
     * @throws NoSuchAlgorithmException 算法异常
     */
    private String generateSignature(String content) throws NoSuchAlgorithmException {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest((content + SECRET_KEY).getBytes());
        
        // 转换为十六进制字符串
        StringBuilder hexString = new StringBuilder();
        for (byte b : hash) {
            String hex = Integer.toHexString(0xff & b);
            if (hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        
        return hexString.toString();
    }
}