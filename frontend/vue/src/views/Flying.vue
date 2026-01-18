<template>
  <div class="flying">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>Drone Live Monitor - {{ userId }}</span>
              <div>
                <el-button @click="$router.push('/')">Back</el-button>
                <el-button 
                  type="primary" 
                  @click="toggleRealTimePrediction" 
                  :loading="realTimePredicting"
                  :type="realTimePredicting ? 'danger' : 'success'"
                  style="margin-left: 10px;">
                  {{ realTimePredicting ? 'Stop Real-time' : 'Start Real-time' }}
                </el-button>
              </div>
            </div>
          </template>
          
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="upload-section">
                <el-tabs v-model="activeTab">
                  <el-tab-pane label="Upload Image" name="upload">
                    <el-upload
                      class="upload-demo"
                      drag
                      :auto-upload="false"
                      :on-change="handleFileChange"
                      accept="image/*"
                    >
                      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                      <div class="el-upload__text">
                        Drop image here or <em>click to upload</em>
                      </div>
                    </el-upload>
                    <el-button type="primary" @click="predict" :loading="predicting" style="margin-top: 10px;">
                      Predict Obstacles
                    </el-button>
                  </el-tab-pane>
                  <el-tab-pane label="Camera" name="camera">
                    <div class="camera-section">
                      <video v-if="cameraActive" ref="videoElement" autoplay playsinline width="100%" height="auto"></video>
                      <div v-else class="camera-placeholder">
                        <el-empty description="Camera is not active"></el-empty>
                      </div>
                      <el-button 
                        type="primary" 
                        @click="toggleCamera" 
                        :disabled="realTimePredicting"
                        style="margin-top: 10px;">
                        {{ cameraActive ? 'Stop Camera' : 'Start Camera' }}
                      </el-button>
                      <el-button 
                        type="success" 
                        @click="captureImage" 
                        :disabled="!cameraActive || realTimePredicting" 
                        style="margin-top: 10px; margin-left: 10px;">
                        Capture Image
                      </el-button>
                    </div>
                  </el-tab-pane>
                </el-tabs>
              </div>
            </el-col>
            
            <el-col :span="12">
              <div class="result-section">
                <h3>Prediction Result</h3>
                <div v-if="resultImage" class="image-container">
                  <img :src="resultImage" alt="Prediction Result" />
                </div>
                <div v-else-if="imageData" class="image-container">
                  <img :src="imageData" alt="Selected Image" />
                </div>
                <div v-else class="placeholder">
                  <el-empty description="No image selected yet"></el-empty>
                </div>
                <div v-if="realTimePredicting" class="real-time-indicator">
                  <el-tag type="warning">Real-time Prediction Active</el-tag>
                  <div class="fps-info">FPS: {{ fps }}</div>
                </div>
              </div>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" style="margin-top: 20px;">
            <el-col :span="24">
              <div v-if="boxes.length > 0">
                <h3>Detected Obstacles ({{ boxes.length }})</h3>
                <el-table :data="boxes" style="width: 100%">
                  <el-table-column prop="class_name" label="Class" width="150"></el-table-column>
                  <el-table-column prop="confidence" label="Confidence" width="120">
                    <template #default="scope">
                      {{ (scope.row.confidence * 100).toFixed(2) }}%
                    </template>
                  </el-table-column>
                  <el-table-column prop="xyxy" label="Bounding Box">
                    <template #default="scope">
                      [{{ scope.row.xyxy.map(x => x.toFixed(0)).join(', ') }}]
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { UploadFilled } from '@element-plus/icons-vue'
import { droneApi } from '../api'

export default {
  name: 'Flying',
  components: {
    UploadFilled
  },
  data() {
    return {
      userId: this.$route.query.userId || 'drone001',
      selectedFile: null,
      imageData: null,
      predicting: false,
      resultImage: null,
      boxes: [],
      activeTab: 'upload',
      cameraActive: false,
      videoStream: null,
      canvas: null,
      realTimePredicting: false,
      realTimeInterval: null,
      fps: 0,
      frameCount: 0,
      lastFpsUpdate: 0,
      refreshInterval: null, // 用于定时刷新预测结果
      refreshIntervalTime: 2000 // 每2秒刷新一次
    }
  },
  mounted() {
    // 初始化canvas元素用于图像捕获
    this.canvas = document.createElement('canvas')
    // 如果用户ID是drone001，自动切换到摄像头标签页
    if (this.userId === 'drone001') {
      this.activeTab = 'camera'
    }
    
    // 启动定时刷新，从后端获取最新的预测结果
    this.startRefreshInterval()
  },
  beforeUnmount() {
    // 组件销毁前清理资源
    this.stopRealTimePrediction()
    this.stopRefreshInterval()
    if (this.videoStream) {
      this.videoStream.getTracks().forEach(track => track.stop())
    }
  },
  methods: {
    handleFileChange(file) {
      this.selectedFile = file.raw
      const reader = new FileReader()
      reader.onload = (e) => {
        this.imageData = e.target.result
      }
      reader.readAsDataURL(this.selectedFile)
    },
    async toggleCamera() {
      if (this.cameraActive) {
        // 关闭摄像头
        if (this.videoStream) {
          this.videoStream.getTracks().forEach(track => track.stop())
          this.videoStream = null
        }
        this.cameraActive = false
        this.$message.success('Camera stopped')
      } else {
        // 启动摄像头
        try {
          const videoElement = this.$refs.videoElement
          if (videoElement) {
            this.videoStream = await navigator.mediaDevices.getUserMedia({ video: true })
            videoElement.srcObject = this.videoStream
            this.cameraActive = true
            this.$message.success('Camera started')
          }
        } catch (error) {
          this.$message.error('Failed to access camera: ' + error.message)
          console.error('Camera error:', error)
        }
      }
    },
    captureImage() {
      const videoElement = this.$refs.videoElement
      if (!videoElement || !this.cameraActive) {
        return
      }
      
      // 设置canvas大小与视频一致
      this.canvas.width = videoElement.videoWidth
      this.canvas.height = videoElement.videoHeight
      
      // 绘制视频帧到canvas
      const ctx = this.canvas.getContext('2d')
      ctx.drawImage(videoElement, 0, 0, this.canvas.width, this.canvas.height)
      
      // 将canvas内容转换为data URL
      this.imageData = this.canvas.toDataURL('image/jpeg')
      this.$message.success('Image captured')
    },
    async predict() {
      if (!this.imageData) {
        this.$message.warning('Please select an image first')
        return
      }
      
      this.predicting = true
      try {
        const response = await droneApi.uploadImage({
          userId: this.userId,
          image: this.imageData,
          token: 'test-token'
        })
        
        if (response.data.code === 200) {
          this.boxes = response.data.data.boxes || []
          this.resultImage = 'data:image/jpeg;base64,' + response.data.data.image
          this.$message.success('Prediction completed')
        } else {
          this.$message.error('Prediction failed')
        }
      } catch (error) {
        this.$message.error('Prediction error: ' + error.message)
      } finally {
        this.predicting = false
      }
    },
    toggleRealTimePrediction() {
      if (this.realTimePredicting) {
        this.stopRealTimePrediction()
      } else {
        this.startRealTimePrediction()
      }
    },
    async startRealTimePrediction() {
      // 如果摄像头未启动，先启动摄像头
      if (!this.cameraActive) {
        await this.toggleCamera()
        if (!this.cameraActive) {
          this.$message.error('Failed to start camera, cannot start real-time prediction')
          return
        }
      }
      
      this.realTimePredicting = true
      this.frameCount = 0
      this.lastFpsUpdate = Date.now()
      this.fps = 0
      
      // 开始实时预测循环
      this.realTimeInterval = setInterval(() => {
        this.realTimePredict()
      }, 100) // 每100ms捕获一帧，约10fps
      
      this.$message.success('Real-time prediction started')
    },
    stopRealTimePrediction() {
      this.realTimePredicting = false
      if (this.realTimeInterval) {
        clearInterval(this.realTimeInterval)
        this.realTimeInterval = null
      }
      this.$message.success('Real-time prediction stopped')
    },
    async realTimePredict() {
      if (!this.cameraActive || !this.realTimePredicting) {
        return
      }
      
      try {
        const videoElement = this.$refs.videoElement
        if (!videoElement) {
          return
        }
        
        // 更新FPS计数
        this.frameCount++
        const now = Date.now()
        if (now - this.lastFpsUpdate >= 1000) {
          this.fps = this.frameCount
          this.frameCount = 0
          this.lastFpsUpdate = now
        }
        
        // 设置canvas大小与视频一致
        this.canvas.width = videoElement.videoWidth
        this.canvas.height = videoElement.videoHeight
        
        // 绘制视频帧到canvas
        const ctx = this.canvas.getContext('2d')
        ctx.drawImage(videoElement, 0, 0, this.canvas.width, this.canvas.height)
        
        // 将canvas内容转换为data URL
        const imageData = this.canvas.toDataURL('image/jpeg')
        
        // 发送到YOLO服务进行预测
        const response = await droneApi.uploadImage({
          userId: this.userId,
          image: imageData,
          token: 'test-token'
        })
        
        if (response.data.code === 200) {
          this.boxes = response.data.data.boxes || []
          this.resultImage = 'data:image/jpeg;base64,' + response.data.data.image
        }
      } catch (error) {
        console.error('Real-time prediction error:', error)
        // 不显示错误消息，避免频繁弹窗
      }
    },
    
    // 启动定时刷新
    startRefreshInterval() {
      if (this.refreshInterval) {
        this.stopRefreshInterval()
      }
      
      this.refreshInterval = setInterval(() => {
        this.refreshPrediction()
      }, this.refreshIntervalTime)
      
      console.log(`定时刷新已启动，每 ${this.refreshIntervalTime}ms 刷新一次`)
    },
    
    // 停止定时刷新
    stopRefreshInterval() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
        this.refreshInterval = null
        console.log('定时刷新已停止')
      }
    },
    
    // 刷新预测结果
    async refreshPrediction() {
      // 实时预测模式下不进行定时刷新，避免冲突
      if (this.realTimePredicting) {
        return
      }
      
      try {
        console.log('刷新预测结果...')
        
        // 1. 先获取最新的预测数据（包含障碍物信息）
        const response = await droneApi.getLatestPrediction({
          userId: this.userId,
          token: 'test-token'
        })
        
        if (response.data.code === 200) {
          const predictionData = response.data.data.prediction
          if (predictionData) {
            this.boxes = predictionData.boxes || []
            console.log('预测结果已更新')
          }
        }
        
        // 2. 直接从固定URL获取带标注的图片，添加时间戳防止缓存
        const timestamp = new Date().getTime()
        const imageUrl = `http://localhost:8080/drone_${this.userId}_yolo.jpg?t=${timestamp}`
        this.resultImage = imageUrl
        console.log('图片已更新:', imageUrl)
        
      } catch (error) {
        console.error('刷新预测结果失败:', error)
      }
    }
  }
}
</script>

<style scoped>
.flying {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-section {
  padding: 20px;
  text-align: center;
}

.result-section {
  padding: 20px;
  text-align: center;
  position: relative;
}

.image-container img {
  max-width: 100%;
  max-height: 400px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-section {
  text-align: center;
}

.camera-section video {
  border: 1px solid #ddd;
  border-radius: 4px;
  max-width: 100%;
  max-height: 300px;
  background-color: #f0f0f0;
}

.camera-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  border: 1px dashed #ddd;
  border-radius: 4px;
}

:deep(.el-tabs__content) {
  margin-top: 10px;
}

.real-time-indicator {
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.fps-info {
  font-size: 14px;
  color: #606266;
  font-weight: bold;
}

/* 实时预测状态下的样式 */
.real-time-active {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 77, 79, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(255, 77, 79, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 77, 79, 0);
  }
}
</style>
